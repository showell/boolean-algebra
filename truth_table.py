from itertools import chain, combinations


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def listify_truth_table(truth_table):
    return sorted(",".join(sorted(s)) for s in truth_table)


def truth_table(expr, variables):
    return {s for s in powerset(variables) if expr.eval(s)}
