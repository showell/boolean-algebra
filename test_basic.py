from basic_bool import TRUE, FALSE, SYMBOL
from lib.test_helpers import run_test, assert_str

T = TRUE
F = FALSE

x = SYMBOL("x")
y = SYMBOL("y")


@run_test
def strings():
    assert_str(T, "T")
    assert_str(F, "F")
    assert_str(T & F, "(T)&(F)")
    assert_str(T | x, "(T)|(x)")
    assert_str(~y | x, "(~y)|(x)")
