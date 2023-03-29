import basic_bool
import bool
from truth_table import truth_table


class BoolWrapper:
    """
    This is mostly used for testing, but it does kind of
    encapsulate the API of our bool class.

    It builds up basic_bool objections in conjunction with
    our regular bool objects using Python's &, |, and ~.
    """

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

    def check(self):
        tvars = self.basic_expr.symbols()
        basic_tt = truth_table(self.basic_expr, tvars)
        tt = truth_table(self.expr, tvars)
        assert basic_tt == tt

    def LOOSENS(self, other):
        return self.expr.LOOSENS(other.expr)

    def RESTRICTS(self, other):
        return self.expr.RESTRICTS(other.expr)


def SYMBOL(name):
    return BoolWrapper(basic_bool.SYMBOL(name), bool.SYMBOL(name))


TRUE = BoolWrapper(basic_bool.TRUE, bool.TRUE)
FALSE = BoolWrapper(basic_bool.FALSE, bool.FALSE)
