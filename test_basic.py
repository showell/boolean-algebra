from basic_bool import TRUE, FALSE, SYMBOL
from lib.test_helpers import run_test, assert_str

T = TRUE
F = FALSE

x = SYMBOL("x")
y = SYMBOL("y")

NEITHER = set()
X = {"x"}
Y = {"y"}
BOTH = {"x", "y"}


@run_test
def strings():
    assert_str(T, "T")
    assert_str(F, "F")
    assert_str(T & F, "(T)&(F)")
    assert_str(T | x, "(T)|(x)")
    assert_str(~y | x, "(~y)|(x)")


@run_test
def eval():
    assert not F.eval(NEITHER)
    assert not F.eval(X)
    assert not F.eval(Y)
    assert not F.eval(BOTH)

    assert T.eval(NEITHER)
    assert T.eval(X)
    assert T.eval(Y)
    assert T.eval(BOTH)

    assert not x.eval(NEITHER)
    assert x.eval(X)
    assert not x.eval(Y)
    assert x.eval(BOTH)

    assert (~x).eval(NEITHER)
    assert not (~x).eval(X)
    assert (~x).eval(Y)
    assert not (~x).eval(BOTH)

    assert not (x & y).eval(NEITHER)
    assert not (x & y).eval(X)
    assert not (x & y).eval(Y)
    assert (x & y).eval(BOTH)

    assert not (x | y).eval(NEITHER)
    assert (x | y).eval(X)
    assert (x | y).eval(Y)
    assert (x | y).eval(BOTH)

    assert (x | ~y).eval(NEITHER)
    assert (x | ~y).eval(X)
    assert not (x | ~y).eval(Y)
    assert (x | ~y).eval(BOTH)
