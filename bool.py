class TrueVal:
    def __str__(self):
        return "T"
    
    def AND(self, other):
        return other

    def OR(self, other):
        return TRUE

    def NOT(self):
        return FALSE


class FalseVal:
    def __str__(self):
        return "F"
    
    def AND(self, other):
        return FALSE

    def OR(self, other):
        return other

    def NOT(self):
        return TRUE

class Expression:
    def AND(self, other):
        if type(other) == TrueVal:
            return self

        if type(other) == FalseVal:
            return FALSE

        if type(other) == Var:
            return self.AND_VAR(other)

        assert False

    def OR(self, other):
        if type(other) == TrueVal:
            return TRUE

        if type(other) == FalseVal:
            return self

        if type(other) == Var:
            return self.OR_VAR(other)

        assert False

    def AND_VAR(self):
        assert False

    def OR_VAR(self):
        assert False

class Var(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def AND_VAR(self, other):
        assert other.name == self.name
        return self

    def OR_VAR(self, other):
        assert other.name == self.name
        return self

TRUE = TrueVal()
FALSE = FalseVal()

def _AND2(a, b):
    return a.AND(b)

def _OR2(a, b):
    return a.OR(b)

def NOT(a):
    return a.NOT()

def AND(*lst):
    assert len(lst) >= 1
    if len(lst) == 1:
        return lst[0] 
    return _AND2(lst[0], AND(*lst[1:]))

def OR(*lst):
    assert len(lst) >= 1
    if len(lst) == 1:
        return lst[0] 
    return _OR2(lst[0], OR(*lst[1:]))

def SYMBOL(name):
    return Var(name)
