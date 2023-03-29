# STRESS TEST
from bool_wrapper import TRUE, FALSE, SYMBOL
from lib.test_helpers import run_test
import solver

T = TRUE
F = FALSE

x = SYMBOL("x")
y = SYMBOL("y")


@run_test
def stress():
    exprs = [T, F, x, y]

    def solutions(v):
        return solver.solutions(v.basic_expr, {"x", "y"})

    slots = {solutions(expr): str(expr) for expr in exprs}
    seen_strs = {str(expr) for expr in exprs}

    def handle(v):
        v.check()
        if str(v) not in seen_strs:
            next_exprs.append(v)
            seen_strs.add(str(v))
            sol = solutions(v)
            if sol in slots:
                print(slots)
                print(v, slots[sol])
                # assert False
            slots[sol] = str(v)

    while len(exprs) < 500:
        next_exprs = []

        for expr in exprs:
            handle(~expr)
            handle(~~expr)

        for a in exprs:
            for b in exprs:
                print(len(seen_strs), sorted(seen_strs))
                print(a, str(a.expr), type(a.expr))
                print(b, str(b.basic_expr), type(b.expr))
                handle(a & b)
                handle(a | b)

        exprs.extend(next_exprs)
