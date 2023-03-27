from bool import TRUE, FALSE, AND, OR, NOT, SYMBOL
from lib.test_helpers import run_test, assert_str

T = TRUE
F = FALSE
x = SYMBOL("x")


@run_test
def simple():
    assert_str(T, "T")
    assert_str(F, "F")
    assert_str(AND(F, T), "F")
    assert_str(OR(F, T), "T")
    assert_str(AND(T, T, F), "F")
    assert_str(OR(F, T, T), "T")

    assert_str(x, "x")
    assert_str(AND(x, x), "x")
    assert_str(OR(x, x), "x")

    assert_str(AND(x, T), "x")
    assert_str(OR(x, T), "T")

    assert_str(AND(x, F), "F")
    assert_str(OR(x, F), "x")


@run_test
def negated_vars():
    assert_str(~x, "~x")

    assert_str(~x & ~x, "~x")
    assert_str(~x | ~x, "~x")


@run_test
def double_negation():
    assert_str(~~x, "x")
    assert_str(~~~~x, "x")

    assert_str(~~~x, "~x")
    assert_str(~~~~~x, "~x")


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
def complementation():
    assert_str(x & ~x, "F")
    assert_str(x | ~x, "T")

    assert_str(~x & x, "F")
    assert_str(~x | x, "T")
