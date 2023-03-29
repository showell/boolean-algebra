from basic_bool import TRUE, FALSE, SYMBOL
from lib.test_helpers import assert_equal, assert_str, run_test
from solver import stringify_solutions, solutions

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


@run_test
def show_solution_output():
    assert_equal(
        solutions(x | y, {"x", "y", "z"}),
        "{x}{x,y}{x,y,z}{x,z}{y}{y,z}",
    )


@run_test
def solve():
    def check(tvar_sets, expr):
        expected_result = stringify_solutions(tvar_sets)
        variables = {"x", "y"}
        tt = solutions(expr, variables)
        assert_equal(expected_result, tt)

    N = NEITHER
    B = BOTH

    check([], F)
    check([N], ~(x | y))
    check([X], x & ~y)
    check([Y], ~x & y)
    check([B], x & y)
    check([N, X], ~y)
    check([N, Y], ~x)
    check([N, B], (~x & ~y) | (x & y))
    check([X, Y], (x | y) & ~(x & y))
    check([X, B], x)
    check([Y, B], y)
    check([N, X, Y], ~x | ~y)
    check([N, X, B], x | ~y)
    check([N, Y, B], ~x | y)
    check([X, Y, B], x | y)
    check([N, X, Y, B], T)
