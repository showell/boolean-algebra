# STRESS TEST
from bool_wrapper import TRUE, FALSE, SYMBOL
from lib.test_helpers import run_test

T = TRUE
F = FALSE

x = SYMBOL("x")
y = SYMBOL("y")


# @run_test
def stress():
    exprs = [T, F, x, y]

    seen_strs = {str(expr) for expr in exprs}

    while len(exprs) < 100:
        next_exprs = []

        for expr in exprs:
            v = ~expr
            next_exprs.append(v)

        for a in exprs:
            for b in exprs:
                print(sorted(seen_strs))
                print(a, type(a.expr))
                print(b, type(b.expr))
                v = a & b
                v.check()
                if str(v) not in seen_strs:
                    next_exprs.append(v)
                    seen_strs.add(str(v))

        exprs.extend(next_exprs)
