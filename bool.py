class Expression:
    def __and__(self, other):
        return self.AND(other)

    def __or__(self, other):
        return self.OR(other)

    def __invert__(self):
        return self.NOT()

    def AND(self, other):
        if type(other) == TrueVal:
            return self

        if type(other) == FalseVal:
            return FALSE

        if type(other) == Var:
            return self.AND_VAR(other)

        if type(other) == NegatedVar:
            return self.AND_NEGATED_VAR(other)

        assert False

    def OR(self, other):
        if type(other) == TrueVal:
            return TRUE

        if type(other) == FalseVal:
            return self

        if type(other) == Var:
            return self.OR_VAR(other)

        if type(other) == NegatedVar:
            return self.OR_NEGATED_VAR(other)

        assert False

    def AND_VAR(self, other):
        assert False

    def OR_VAR(self, other):
        assert False

    def AND_NEGATED_VAR(self, other):
        assert False

    def OR_NEGATED_VAR(self, other):
        assert False


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


class Var(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def AND_VAR(self, other):
        assert other.name == self.name
        return self

    def OR_VAR(self, other):
        assert other.name == self.name
        return self

    def AND_NEGATED_VAR(self, other):
        assert other.name == self.name
        return FALSE

    def OR_NEGATED_VAR(self, other):
        assert other.name == self.name
        return TRUE

    def NOT(self):
        return NegatedVar(self.name)


class NegatedVar(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "~" + self.name

    def AND_VAR(self, other):
        assert other.name == self.name
        return FALSE

    def OR_VAR(self, other):
        assert other.name == self.name
        return TRUE

    def AND_NEGATED_VAR(self, other):
        assert other.name == self.name
        return self

    def OR_NEGATED_VAR(self, other):
        assert other.name == self.name
        return self

    def NOT(self):
        return Var(self.name)


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
    return Var(name)
