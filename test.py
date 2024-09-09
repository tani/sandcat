from sandcat import Atom, check

A, B, C = Atom("A"), Atom("B"), Atom("C")


# Test w.r.t. the above example
assert check([C << A, B, A], C, algorithm="z3") is False
assert check([C << A, A, B], C, algorithm="z3") is True
assert check([C << A, A, C >> C], C, algorithm="z3") is True
