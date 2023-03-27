from bool import TRUE, FALSE, SYMBOL
from lib.test_helpers import run_test, assert_str

T = TRUE
F = FALSE
x = SYMBOL("x")
y = SYMBOL("y")
z = SYMBOL("z")


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


@run_test
def simple_or_clauses():
    assert_str(x | y, "x|y")
    assert_str(z | y | x, "x|y|z")
