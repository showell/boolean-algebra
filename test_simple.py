from bool import TRUE, FALSE, AND, OR, NOT
from lib.test_helpers import run_test, assert_str

@run_test
def simple():
    T = TRUE
    F = FALSE 
    assert_str(T, "T")
    assert_str(F, "F")
    assert_str(AND(F, T), "F")
    assert_str(OR(F, T), "T")
    assert_str(AND(T, T, F), "F")
    assert_str(OR(F, T, T), "T")


