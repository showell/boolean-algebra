from basic_bool import TRUE, FALSE, SYMBOL
from lib.test_helpers import assert_equal, assert_str, run_test
from solver import stringify_solutions, solutions

T = TRUE
F = FALSE

x = SYMBOL("x")
y = SYMBOL("y")

FF = set()
TF = {"x"}
FT = {"y"}
TT = {"x", "y"}


@run_test
def strings():
    assert_str(T, "T")
    assert_str(F, "F")
    assert_str(T & F, "(T)&(F)")
    assert_str(T | x, "(T)|(x)")
    assert_str(~y | x, "(~y)|(x)")


@run_test
def symbols():
    assert_equal(
        (~y | x).symbols(),
        {"x", "y"},
    )


@run_test
def eval():
    assert not F.eval(FF)
    assert not F.eval(TF)
    assert not F.eval(FT)
    assert not F.eval(TT)

    assert T.eval(FF)
    assert T.eval(TF)
    assert T.eval(FT)
    assert T.eval(TT)

    assert not x.eval(FF)
    assert x.eval(TF)
    assert not x.eval(FT)
    assert x.eval(TT)

    assert (~x).eval(FF)
    assert not (~x).eval(TF)
    assert (~x).eval(FT)
    assert not (~x).eval(TT)

    assert not (x & y).eval(FF)
    assert not (x & y).eval(TF)
    assert not (x & y).eval(FT)
    assert (x & y).eval(TT)

    assert not (x | y).eval(FF)
    assert (x | y).eval(TF)
    assert (x | y).eval(FT)
    assert (x | y).eval(TT)

    assert (x | ~y).eval(FF)
    assert (x | ~y).eval(TF)
    assert not (x | ~y).eval(FT)
    assert (x | ~y).eval(TT)


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

    check([], F)
    check([FF], ~(x | y))
    check([FT], ~x & y)
    check([TF], x & ~y)
    check([TT], x & y)
    check([FF, FT], ~x)
    check([FF, TF], ~y)
    check([TF, TT], x)
    check([FT, TT], y)
    check([TF, FT], (x | y) & (~x | ~y))
    check([FF, TT], (~x & ~y) | (x & y))
    check([FF, FT, TT], ~x | y)
    check([FF, TF, FT], ~x | ~y)
    check([FF, TF, TT], x | ~y)
    check([TF, FT, TT], x | y)
    check([FF, TF, FT, TT], T)
