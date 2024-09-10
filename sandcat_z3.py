from z3 import And, Bool, BoolRef, Implies, Not, Or, Solver, unsat

from category import Atom, Category, Left, Right


def translate(i: int, cat: Category) -> BoolRef:
    match cat:
        case Atom(name):
            return Bool(f"{name}{i}")
        case Left(lhs, rhs):
            return Implies(translate(i + 1, rhs), translate(i, lhs))
        case Right(lhs, rhs):
            return Implies(translate(i - 1, lhs), translate(i, rhs))


def check(cats: list[Category], cat: Category) -> bool:
    lhs = And(*[translate(i, cat) for (i, cat) in enumerate(cats)])
    rhs = Or(*[translate(i, cat) for i in range(len(cats))])
    solver = Solver()
    solver.add(Not(Implies(lhs, rhs)))
    return solver.check() == unsat
