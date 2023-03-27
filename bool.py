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

        if type(other) == AndClause:
            return self.AND_AND_CLAUSE(other).simplify()

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

        if type(other) == AndClause:
            return self.OR_AND_CLAUSE(other).simplify()

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
        return AndClause([self, other])

    def OR_SIGNED_VAR(self, other):
        if other.name == self.name:
            return self if self.sign == other.sign else TRUE
        return OrClause([self, other])

    def OR_OR_CLAUSE(self, other):
        return other.OR_SIGNED_VAR(self)

    def AND_OR_CLAUSE(self, other):
        return other.AND_SIGNED_VAR(self)

    def AND_AND_CLAUSE(self, other):
        return other.AND_SIGNED_VAR(self)

    def OR_AND_CLAUSE(self, other):
        return other.OR_SIGNED_VAR(self)

    def NOT(self):
        return SignedVar(self.name, not self.sign)


class Clause(Expression):
    def __init__(self, signed_vars):
        self.signed_vars = signed_vars
        names = {sv.name for sv in signed_vars if sv.sign}
        negated_names = {sv.name for sv in signed_vars if not sv.sign}
        assert not (names & negated_names)
        self.names = names
        self.negated_names = negated_names

    def stringified_vars(self):
        signed_vars = sorted(list(self.signed_vars), key=lambda sv: sv.name)
        return [str(sv) for sv in signed_vars]

    def simplify(self):
        if len(self.signed_vars) == 1:
            return self.signed_vars[0]
        return self

    @staticmethod
    def make_signed_vars(names, negated_names):
        return [SignedVar(name, True) for name in names] + [
            SignedVar(name, False) for name in negated_names
        ]


class OrClause(Clause):
    def __str__(self):
        return "|".join(self.stringified_vars())

    def AND_SIGNED_VAR(self, other):
        found = False
        signed_vars = []
        for sv in self.signed_vars:
            if sv.name == other.name:
                if sv.sign == other.sign:
                    return other
                else:
                    found = True
            else:
                signed_vars.append(sv)
        if found:
            return OrClause(signed_vars)
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
        signed_vars = Clause.make_signed_vars(names, negated_names)
        return OrClause(signed_vars)


class AndClause(Clause):
    def __str__(self):
        return "&".join(self.stringified_vars())

    def OR_SIGNED_VAR(self, other):
        found = False
        signed_vars = []
        for sv in self.signed_vars:
            if sv.name == other.name:
                if sv.sign == other.sign:
                    return other
                else:
                    found = True
            else:
                signed_vars.append(sv)
        if found:
            return AndClause(signed_vars)
        assert False

    def AND_SIGNED_VAR(self, other):
        return self.AND_AND_CLAUSE(AndClause([other]))

    def AND_AND_CLAUSE(self, other):
        names = self.names | other.names
        negated_names = self.negated_names | other.negated_names
        if names & negated_names:
            return FALSE
        return AndClause.make(names, negated_names)

    @staticmethod
    def make(names, negated_names):
        signed_vars = Clause.make_signed_vars(names, negated_names)
        return AndClause(signed_vars)


TRUE = TrueVal()
FALSE = FalseVal()


def SYMBOL(name):
    return SignedVar(name, True)
