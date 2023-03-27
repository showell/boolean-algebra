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
