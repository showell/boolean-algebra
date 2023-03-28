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
        return dispatch_and(self, other)

    def OR(self, other):
        return dispatch_or(self, other)


class TrueVal(Expression):
    def __str__(self):
        return "T"

    def NOT(self):
        return FALSE


class FalseVal(Expression):
    def __str__(self):
        return "F"

    def NOT(self):
        return TRUE


class SignedVar(Expression):
    def __init__(self, name, sign):
        self.name = name
        self.sign = sign

    def __str__(self):
        return self.name if self.sign else "~" + self.name

    def NOT(self):
        return SignedVar(self.name, not self.sign)


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

    @staticmethod
    def make(names, negated_names):
        signed_vars = Clause.make_signed_vars(names, negated_names)
        return OrClause(signed_vars)


class AndClause(Clause):
    def __str__(self):
        return "&".join(self.stringified_vars())

    def NOT(self):
        return OrClause.make(self.negated_names, self.names)

    @staticmethod
    def make(names, negated_names):
        signed_vars = Clause.make_signed_vars(names, negated_names)
        return AndClause(signed_vars)


TRUE = TrueVal()
FALSE = FalseVal()


def SYMBOL(name):
    return SignedVar(name, True)


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
    for sv in clause.signed_vars:
        if sv.name == signed_var.name:
            if sv.sign == signed_var.sign:
                return signed_var
            else:
                break
    return None


@_AND(OrClause, SignedVar)
def OrClause_AND_SignedVar(clause, signed_var):
    for sv in clause.signed_vars:
        if sv.name == signed_var.name:
            if sv.sign == signed_var.sign:
                return signed_var
            else:
                break
    return None


@_OR(OrClause, SignedVar)
def OrClause_OR_SignedVar(clause, signed_var):
    return OrClause_OR_OrClause(clause, OrClause([signed_var]))


@_AND(AndClause, SignedVar)
def AndClause_AND_SignedVar(clause, signed_var):
    return AndClause_AND_AndClause(clause, AndClause([signed_var]))
