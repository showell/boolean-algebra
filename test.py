import basic_bool
import bool
from lib.test_helpers import run_test, assert_str
from truth_table import listify_truth_table, truth_table


class BoolWrapper:
    def __init__(self, basic_expr, expr):
        self.basic_expr = basic_expr
        self.expr = expr

    def __str__(self):
        return str(self.expr)

    def __and__(self, other):
        return BoolWrapper(
            self.basic_expr & other.basic_expr,
            self.expr & other.expr,
        )

    def __or__(self, other):
        return BoolWrapper(
            self.basic_expr | other.basic_expr,
            self.expr | other.expr,
        )

    def __invert__(self):
        return BoolWrapper(~self.basic_expr, ~self.expr)

    def LOOSENS(self, other):
        return self.expr.LOOSENS(other.expr)

    def RESTRICTS(self, other):
        return self.expr.RESTRICTS(other.expr)

    @staticmethod
    def SYMBOL(name):
        return BoolWrapper(basic_bool.SYMBOL(name), bool.SYMBOL(name))


T = BoolWrapper(basic_bool.TRUE, bool.TRUE)
F = BoolWrapper(basic_bool.FALSE, bool.FALSE)

w = BoolWrapper.SYMBOL("w")
x = BoolWrapper.SYMBOL("x")
y = BoolWrapper.SYMBOL("y")
z = BoolWrapper.SYMBOL("z")


@run_test
def associativity():
    assert_str(x & (y & z), "x&y&z")
    assert_str(x | (y | z), "x|y|z")

    assert_str(x & (z & y), "x&y&z")
    assert_str(x | (z | y), "x|y|z")

    assert_str((x & z) & y, "x&y&z")
    assert_str((x | z) | y, "x|y|z")


@run_test
def commutativity():
    assert_str(y & x, "x&y")
    assert_str(x & y, "x&y")
    assert_str(z & x & y, "x&y&z")

    assert_str(y | x, "x|y")
    assert_str(x | y, "x|y")
    assert_str(z | x | y, "x|y|z")


@run_test
def distributivity():
    assert_str(x & (z | y), "(x&y)|(x&z)")
    assert_str(x | (z & y), "(x|y)&(x|z)")


@run_test
def identity():
    assert_str(x & T, "x")
    assert_str(x | F, "x")


@run_test
def annihilator():
    assert_str(x & F, "F")
    assert_str(x | T, "T")


@run_test
def idemptotence():
    assert_str(x & x, "x")
    assert_str(x | x, "x")


@run_test
def absorption():
    assert_str((x | y) & x, "x")
    assert_str(x & (x | y), "x")
    assert_str(x | (x & y), "x")
    assert_str((x & y) | x, "x")


@run_test
def negative_absorption():
    assert_str(x & (~x | y), "x&y")
    assert_str((~x | y) & x, "x&y")

    assert_str(x | (~x & y), "x|y")
    assert_str((~x & y) | x, "x|y")


@run_test
def complementation():
    assert_str(x & ~x, "F")
    assert_str(x | ~x, "T")

    assert_str(~x & x, "F")
    assert_str(~x | x, "T")


@run_test
def double_negation():
    assert_str(~~x, "x")
    assert_str(~~~~x, "x")

    assert_str(~~~x, "~x")
    assert_str(~~~~~x, "~x")

    assert_str(~~~~(x | y | z), "x|y|z")
    assert_str(~~~~(x & y & z), "x&y&z")


@run_test
def de_morgan():
    assert_str(~(x & y), "~x|~y")
    assert_str(~(x | y), "~x&~y")


@run_test
def elimination():
    assert_str((x & y) | (x & ~y), "x")
    assert_str((x | y) & (x | ~y), "x")


# OTHER


@run_test
def negated_vars():
    assert_str(~x, "~x")

    assert_str(~x & ~x, "~x")
    assert_str(~x | ~x, "~x")


@run_test
def restriction():
    assert not T.RESTRICTS(x)
    assert not x.RESTRICTS(y)
    assert not x.RESTRICTS(y & z)
    assert not (y & x).RESTRICTS(z)
    assert not x.RESTRICTS(~x)
    assert not x.RESTRICTS(y | z)
    assert not (x & y & z).RESTRICTS(w & x)
    assert not (x | w).RESTRICTS(x | y | z)

    assert F.RESTRICTS(T)
    assert F.RESTRICTS(x)
    assert F.RESTRICTS(x & y)
    assert x.RESTRICTS(T)
    assert (x & y).RESTRICTS(x)
    assert x.RESTRICTS(x)
    assert x.RESTRICTS(x | y)
    assert (x | y).RESTRICTS(x | y | z)
    assert (x & y & z).RESTRICTS(x & y)

    assert T.LOOSENS(F)
    assert T.LOOSENS(x)
    assert T.LOOSENS(x | y)
    assert (x | y).LOOSENS(x)


@run_test
def reductions():
    assert_str((x & y) & (x & y & z), "x&y&z")
    assert_str((x & y & z) & (x & y), "x&y&z")
    assert_str((~w & x & y & z) & (x & y), "~w&x&y&z")

    assert_str((x | y) | (x | y | z), "x|y|z")
    assert_str((x | y | z) | (x | y), "x|y|z")
    assert_str((~w | x | y | z) | (x | y), "~w|x|y|z")


@run_test
def advanced_de_morgan():
    assert_str(x | (z & y), "(x|y)&(x|z)")
    assert_str(~(x | (y & z)), "(~x&~y)|(~x&~z)")

    assert_str(x & (z | y), "(x&y)|(x&z)")
    assert_str(~(x & (z | y)), "(~x|~y)&(~x|~z)")


@run_test
def simple_or_clauses():
    assert_str(x | y, "x|y")
    assert_str(z | y | x, "x|y|z")


@run_test
def negated_or_clauses():
    assert_str(x | ~y, "x|~y")
    assert_str(~y | x, "x|~y")

    assert_str(z | x | ~y, "x|~y|z")
    assert_str(z | ~y | x, "x|~y|z")

    assert_str(z | x | ~y | w, "w|x|~y|z")
    assert_str(z | x | ~y | ~w, "~w|x|~y|z")

    assert_str(z | x | ~y | w | z, "w|x|~y|z")
    assert_str(z | x | ~y | ~w | z, "~w|x|~y|z")

    assert_str((z | x) | (~y | w | z), "w|x|~y|z")
    assert_str((z | x) | (~y | ~w | z), "~w|x|~y|z")

    assert_str((z | x) | ~x, "T")
    assert_str((~z | x) | (y | ~z), "x|y|~z")
    assert_str((x | z) | (x | ~z), "T")


@run_test
def negated_and():
    assert_str((z & x) & ~x, "F")


@run_test
def simple_and_clauses():
    assert_str(x & y, "x&y")
    assert_str(x & y & z, "x&y&z")
    assert_str(z & x & y, "x&y&z")
    assert_str((z & x) & y, "x&y&z")
    assert_str((z & x) & (y & w), "w&x&y&z")
    assert_str((z & x) & (y & ~w), "~w&x&y&z")
    assert_str((z & x) & (y & ~w) & T, "~w&x&y&z")
    assert_str((z & x) & (y & ~w) & F, "F")
