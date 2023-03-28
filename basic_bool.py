class Expression:
    def __and__(self, other):
        return self.AND(other)

    def __or__(self, other):
        return self.OR(other)

    def __invert__(self):
        return self.NOT()

    def AND(self, other):
        return AndPair(self, other)

    def OR(self, other):
        return OrPair(self, other)

    def NOT(self):
        return Negated(self)

    def symbols(self):
        return set()


class TrueVal(Expression):
    def __str__(self):
        return "T"


class FalseVal(Expression):
    def __str__(self):
        return "F"


class Negated(Expression):
    def __init__(self, x):
        self.x = x

    def __str__(self):
        return "~" + str(self.x)


class Symbol(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def symbols(self):
        return {self.name}


class Pair(Expression):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def string_variables(self):
        return [f"({self.x})", f"({self.y})"]

    def symbols(self):
        return self.x.symbols() | self.y.symbols()

    def __str__(self):
        op = self.operator
        return op.join(self.string_variables())

class AndPair(Pair):
    operator = "&"


class OrPair(Pair):
    operator = "|"


TRUE = TrueVal()
FALSE = FalseVal()


def SYMBOL(name):
    return Symbol(name)
