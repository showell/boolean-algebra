_AND_TUPLES = []
_OR_TUPLES = []


def dispatch(tuples, x, y):
    for (
        type1,
        type2,
        f,
    ) in tuples:
        if isinstance(x, type1) and isinstance(y, type2):
            result = f(x, y)
            if result is not None:
                return result
        if isinstance(x, type2) and isinstance(y, type1):
            result = f(y, x)
            if result is not None:
                return result
    assert False


def dispatch_and(x, y):
    return dispatch(_AND_TUPLES, x, y)


def dispatch_or(x, y):
    return dispatch(_OR_TUPLES, x, y)


def _AND(type1, type2):
    def wrap(f):
        assert f.__name__ == type1.__name__ + "_AND_" + type2.__name__
        _AND_TUPLES.append((type1, type2, f))
        return f

    return wrap


def _OR(type1, type2):
    def wrap(f):
        assert f.__name__ == type1.__name__ + "_OR_" + type2.__name__
        _OR_TUPLES.append((type1, type2, f))
        return f

    return wrap
