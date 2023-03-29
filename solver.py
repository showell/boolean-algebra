from itertools import chain, combinations

"""
This module finds all combinations of variables that satisfy
a boolean expression.

It does this by brute force. It computes the powerset of
variables (just as if you were constructing an explicit
truth table on a chalkboard), then evaluates the expression
for each possible subset of variables being assigned to True.
"""


def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def braced(s):
    return "{" + s + "}"


def stringify_solutions(solutions):
    sorted_solutions = sorted(",".join(sorted(s)) for s in solutions)
    return "".join(braced(s) for s in sorted_solutions)


def solutions(expr, variables):
    """
    solutions(x | y, {"x", "y", "z"}) ==
    "{x}{x,y}{x,y,z}{x,z}{y}{y,z}",
    """
    return stringify_solutions(s for s in powerset(variables) if expr.eval(s))
