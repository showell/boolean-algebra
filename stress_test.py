# STRESS TEST
from bool_wrapper import TRUE, FALSE, SYMBOL
from lib.test_helpers import run_test

T = TRUE
F = FALSE

x = SYMBOL("x")
y = SYMBOL("y")


@run_test
def stress():
    exprs = [T, F, x, y]

    seen_strs = {str(expr) for expr in exprs}

    def handle(v):
        v.check()
        if str(v) not in seen_strs:
            next_exprs.append(v)
            seen_strs.add(str(v))

    while len(exprs) < 500:
        next_exprs = []

        for expr in exprs:
            v = ~expr
            handle(v)

        for a in exprs:
            for b in exprs:
                print(len(seen_strs), sorted(seen_strs))
                print(a, type(a.expr))
                print(b, type(b.expr))
                handle(a & b)
                handle(a | b)

        exprs.extend(next_exprs)
