class Expression:
    def __and__(self, other):
        return AndPair(self, other)

    def __or__(self, other):
        return OrPair(self, other)

    def __invert__(self):
        return Negated(self)

    def symbols(self):
        return set()


class TrueVal(Expression):
    def __str__(self):
        return "T"

    def eval(self, _):
        return True


class FalseVal(Expression):
    def __str__(self):
        return "F"

    def eval(self, _):
        return False


class Negated(Expression):
    def __init__(self, x):
        self.x = x

    def __str__(self):
        return "~" + str(self.x)

    def symbols(self):
        return self.x.symbols()

    def eval(self, tvars):
        return not self.x.eval(tvars)


class Symbol(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def symbols(self):
        return {self.name}

    def eval(self, tvars):
        return self.name in tvars


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

    def eval(self, tvars):
        return self.x.eval(tvars) and self.y.eval(tvars)


class OrPair(Pair):
    operator = "|"

    def eval(self, tvars):
        return self.x.eval(tvars) or self.y.eval(tvars)


TRUE = TrueVal()
FALSE = FalseVal()


def SYMBOL(name):
    return Symbol(name)
