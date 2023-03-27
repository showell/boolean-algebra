class Expression:
    def __and__(self, other):
        return self.AND(other)

    def __or__(self, other):
        return self.OR(other)

    def __invert__(self):
        return self.NOT()

    def simplify(self):
        return self

    def AND(self, other):
        if type(other) == TrueVal:
            return self

        if type(other) == FalseVal:
            return FALSE

        if type(other) == SignedVar:
            return self.AND_SIGNED_VAR(other)

        if type(other) == OrClause:
            return self.AND_OR_CLAUSE(other).simplify()

        assert False

    def OR(self, other):
        if type(other) == TrueVal:
            return TRUE

        if type(other) == FalseVal:
            return self

        if type(other) == SignedVar:
            return self.OR_SIGNED_VAR(other)

        if type(other) == OrClause:
            return self.OR_OR_CLAUSE(other).simplify()

        assert False

    def NOT(self):
        assert False

    def OR_OR_CLAUSE(self, other):
        return False


class TrueVal(Expression):
    def __str__(self):
        return "T"

    def AND(self, other):
        return other

    def OR(self, other):
        return TRUE

    def NOT(self):
        return FALSE


class FalseVal(Expression):
    def __str__(self):
        return "F"

    def AND(self, other):
        return FALSE

    def OR(self, other):
        return other

    def NOT(self):
        return TRUE

class SignedVar(Expression):
    def __init__(self, name, sign):
        self.name = name
        self.sign = sign

    def __str__(self):
        return self.name if self.sign else "~" + self.name

    def AND_SIGNED_VAR(self, other):
        if other.name == self.name:
            return self if self.sign == other.sign else FALSE
        assert False
 
    def OR_SIGNED_VAR(self, other):
        if other.name == self.name:
            return self if self.sign == other.sign else TRUE
        return OrClause([self, other])

    def OR_OR_CLAUSE(self, other):
        return other.OR_SIGNED_VAR(self)

    def AND_OR_CLAUSE(self, other):
        return other.AND_SIGNED_VAR(self)

    def NOT(self):
        return SignedVar(self.name, not self.sign)
        

class OrClause(Expression):
    def __init__(self, signed_vars):
        self.signed_vars = signed_vars
        names = {sv.name for sv in signed_vars if sv.sign}
        negated_names = {sv.name for sv in signed_vars if not sv.sign}
        assert not (names & negated_names)
        self.names = names
        self.negated_names = negated_names

    def __str__(self):
        signed_vars = sorted(list(self.signed_vars), key=lambda sv: sv.name)
        return "|".join(str(sv) for sv in signed_vars)

    def AND_SIGNED_VAR(self, other):
        for sv in self.signed_vars:
            if sv.name == other.name:
                if sv.sign == other.sign:
                    return other
                else:
                    assert False
        assert False

    def OR_SIGNED_VAR(self, other):
        return self.OR_OR_CLAUSE(OrClause([other]))

    def OR_OR_CLAUSE(self, other):
        names = self.names | other.names
        negated_names = self.negated_names | other.negated_names
        if names & negated_names:
            return TRUE
        return OrClause.make(names, negated_names)

    @staticmethod
    def make(names, negated_names):
        signed_vars = [SignedVar(name, True) for name in names] + [SignedVar(name, False) for name in negated_names]
        return OrClause(signed_vars)
        


TRUE = TrueVal()
FALSE = FalseVal()


def _AND2(a, b):
    return a.AND(b)


def _OR2(a, b):
    return a.OR(b)


def NOT(a):
    return a.NOT()


def AND(*lst):
    assert len(lst) >= 1
    if len(lst) == 1:
        return lst[0]
    return _AND2(lst[0], AND(*lst[1:]))


def OR(*lst):
    assert len(lst) >= 1
    if len(lst) == 1:
        return lst[0]
    return _OR2(lst[0], OR(*lst[1:]))


def SYMBOL(name):
    return SignedVar(name, True)
