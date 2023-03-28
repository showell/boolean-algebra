from dispatcher import (
    _AND,
    _OR,
    dispatch_and,
    dispatch_or,
)


class Expression:
    def __and__(self, other):
        return self.AND(other)

    def __or__(self, other):
        return self.OR(other)

    def __invert__(self):
        return self.NOT()

    def AND(self, other):
        if self.RESTRICTS(other):
            return self
        if other.RESTRICTS(self):
            return other
        return dispatch_and(self, other)

    def OR(self, other):
        if self.LOOSENS(other):
            return self
        if other.LOOSENS(self):
            return other
        return dispatch_or(self, other)

    def IS_TRUE(self):
        return False

    def IS_FALSE(self):
        return False

    def RESTRICTS(self, other):
        return False

    def LOOSENS(self, other):
        return other.RESTRICTS(self)


class TrueVal(Expression):
    def __str__(self):
        return "T"

    def NOT(self):
        return FALSE

    def IS_TRUE(self):
        return True


class FalseVal(Expression):
    def __str__(self):
        return "F"

    def NOT(self):
        return TRUE

    def IS_FALSE(self):
        return True

    def RESTRICTS(self, other):
        return True


class SignedVar(Expression):
    def __init__(self, name, sign):
        self.name = name
        self.sign = sign

    def __str__(self):
        return self.name if self.sign else "~" + self.name

    def EQ(self, other):
        return self.name == other.name and self.sign == other.sign

    def NOT(self):
        return SignedVar(self.name, not self.sign)

    def RESTRICTS(self, other):
        if other.IS_TRUE():
            return True
        if type(other) == SignedVar:
            return self.EQ(other)
        if type(other) == OrClause:
            return any(sv.EQ(self) for sv in other.signed_vars)
        return False


class Clause(Expression):
    def __init__(self, signed_vars):
        for sv in signed_vars:
            assert type(sv) == SignedVar
        self.signed_vars = signed_vars
        names = {sv.name for sv in signed_vars if sv.sign}
        negated_names = {sv.name for sv in signed_vars if not sv.sign}
        assert not (names & negated_names)
        self.names = names
        self.negated_names = negated_names

    def stringified_vars(self):
        signed_vars = sorted(list(self.signed_vars), key=lambda sv: sv.name)
        return [str(sv) for sv in signed_vars]

    def key(self):
        var_names = {sv.name for sv in self.signed_vars}
        return sorted(var_names)

    @staticmethod
    def make_signed_vars(names, negated_names):
        return [SignedVar(name, True) for name in names] + [
            SignedVar(name, False) for name in negated_names
        ]


class OrClause(Clause):
    def __str__(self):
        return "|".join(self.stringified_vars())

    def NOT(self):
        return AndClause.make(self.negated_names, self.names)

    def RESTRICTS(self, other):
        if other.IS_TRUE():
            return True
        if type(other) == SignedVar:
            return all(sv.EQ(other) for sv in self.signed_vars)
        if type(other) == OrClause:
            return all(sv.RESTRICTS(other) for sv in self.signed_vars)
        return False

    @staticmethod
    def make(names, negated_names):
        signed_vars = Clause.make_signed_vars(names, negated_names)
        return OrClause(signed_vars)


class AndClause(Clause):
    def __str__(self):
        return "&".join(self.stringified_vars())

    def NOT(self):
        return OrClause.make(self.negated_names, self.names)

    def RESTRICTS(self, other):
        if other.IS_TRUE():
            return True
        if type(other) == SignedVar:
            return any(sv.EQ(other) for sv in self.signed_vars)
        if type(other) == AndClause:
            return all(self.RESTRICTS(sv) for sv in other.signed_vars)
        return False

    @staticmethod
    def make(names, negated_names):
        signed_vars = Clause.make_signed_vars(names, negated_names)
        return AndClause(signed_vars)


class Junction(Expression):
    def __init__(self, clauses):
        self.clauses = clauses

    def stringified_clauses(self):
        clauses = sorted(self.clauses, key=lambda clause: clause.key())
        return [f"({clause})" for clause in clauses]


class Disjunction(Junction):
    def __str__(self):
        return "|".join(self.stringified_clauses())

    def NOT(self):
        return Conjunction([clause.NOT() for clause in self.clauses])


class Conjunction(Junction):
    def __str__(self):
        return "&".join(self.stringified_clauses())

    def NOT(self):
        return Disjunction([clause.NOT() for clause in self.clauses])


TRUE = TrueVal()
FALSE = FalseVal()


def SYMBOL(name):
    return SignedVar(name, True)


def eliminate_terms(exprs, predicate):
    reject_tups = set()
    for i in range(len(exprs)):
        for j in range(len(exprs)):
            if i != j and (j, i) not in reject_tups:
                if predicate(exprs[i], exprs[j]):
                    reject_tups.add((i, j))

    rejects = {i for i, j in reject_tups}
    return [exprs[i] for i in range(len(exprs)) if i not in rejects]


def eliminate_resticting_terms(exprs):
    return eliminate_terms(exprs, lambda x, y: x.RESTRICTS(y))


def eliminate_loosening_terms(exprs):
    return eliminate_terms(exprs, lambda x, y: x.LOOSENS(y))


def and_expression(exprs):
    exprs = eliminate_loosening_terms(exprs)
    if len(exprs) == 1:
        return exprs[0]
    return Conjunction(exprs)


def or_expression(exprs):
    exprs = eliminate_resticting_terms(exprs)
    if len(exprs) == 1:
        return exprs[0]
    return Disjunction(exprs)


@_AND(TrueVal, Expression)
def TrueVal_AND_Expression(_, x):
    return x


@_AND(FalseVal, Expression)
def FalseVal_AND_Expression(_, x):
    return FALSE


@_OR(TrueVal, Expression)
def TrueVal_OR_Expression(_, x):
    return TRUE


@_OR(FalseVal, Expression)
def FalseVal_OR_Expression(_, x):
    return x


@_AND(SignedVar, SignedVar)
def SignedVar_AND_SignedVar(x, y):
    if x.name == y.name:
        return x if x.sign == y.sign else FALSE
    return AndClause([x, y])


@_OR(SignedVar, SignedVar)
def SignedVar_OR_SignedVar(x, y):
    if x.name == y.name:
        return x if x.sign == y.sign else TRUE
    return OrClause([x, y])


@_AND(AndClause, AndClause)
def AndClause_AND_AndClause(x, y):
    names = x.names | y.names
    negated_names = x.negated_names | y.negated_names
    if names & negated_names:
        return FALSE
    return AndClause.make(names, negated_names)


@_OR(OrClause, OrClause)
def OrClause_OR_OrClause(x, y):
    names = x.names | y.names
    negated_names = x.negated_names | y.negated_names
    if names & negated_names:
        return TRUE
    return OrClause.make(names, negated_names)


@_OR(AndClause, SignedVar)
def AndClause_OR_SignedVar(clause, signed_var):
    exprs = [sv.OR(signed_var) for sv in clause.signed_vars]
    return and_expression(exprs)


@_OR(AndClause, AndClause)
def AndClause_OR_AndClause(x, y):
    exprs = [x.OR(sv) for sv in y.signed_vars]
    return and_expression(exprs)


@_AND(OrClause, SignedVar)
def OrClause_AND_SignedVar(clause, signed_var):
    exprs = [sv.AND(signed_var) for sv in clause.signed_vars]
    return or_expression(exprs)


@_AND(OrClause, OrClause)
def OrClause_AND_OrClause(x, y):
    exprs = [x.AND(sv) for sv in y.signed_vars]
    return or_expression(exprs)


@_OR(OrClause, SignedVar)
def OrClause_OR_SignedVar(clause, signed_var):
    return OrClause_OR_OrClause(clause, OrClause([signed_var]))


@_AND(AndClause, SignedVar)
def AndClause_AND_SignedVar(clause, signed_var):
    return AndClause_AND_AndClause(clause, AndClause([signed_var]))
