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

        if type(other) == OrClause:
            return self.AND_OR_CLAUSE(other).simplify()

        assert False

    def OR(self, other):
        if type(other) == TrueVal:
            return TRUE

        if type(other) == FalseVal:
            return self

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


class OrClause(Expression):
    def __init__(self, names, negated_names):
        self.names = sorted(names)
        self.negated_names = sorted(negated_names)

    def __str__(self):
        pos = self.names
        neg = ["~" + name for name in self.negated_names]
        return "|".join(pos + neg)

    def simplify(self):
        names = list(sorted(self.names))
        negated_names = list(sorted(self.negated_names))
        if names == self.names and negated_names == self:
            return self

        if names or negated_names:
            return OrClause(names, negated_names)

        return TRUE

    def tups(self):
        return [(True, name) for name in self.names] + [
            (False, name) for name in self.negated_names
        ]

    def OR_OR_CLAUSE(self, other):
        names = set(self.names) | set(other.names)
        negated_names = set(self.negated_names) | set(other.negated_names)
        if names & negated_names:
            return TRUE
        return OrClause(names, negated_names)

    def AND_OR_CLAUSE(self, other):
        names = []
        negated_names = []
        for self_sign, self_name in self.tups():
            for other_sign, other_name in other.tups():
                assert self_name == other_name
                if self_name == other_name:
                    if self_sign != other_sign:
                        return FALSE
                    if self_sign:
                        names.append(self_name)
                    else:
                        negated_names.append(self_name)

        return OrClause(names, negated_names)

    def NOT(self):
        if len(self.names) == 1 and len(self.negated_names) == 0:
            return OrClause([], self.names)
        if len(self.names) == 0 and len(self.negated_names) == 1:
            return OrClause(self.negated_names, [])
        assert False


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
    return OrClause([name], [])
