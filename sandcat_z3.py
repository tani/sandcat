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


def check(antecedent: list[Category], succedent: Category) -> bool:
    lhs = And(*[translate(i, cat) for (i, cat) in enumerate(antecedent)])
    rhs = Or(*[translate(i, succedent) for (i, _) in enumerate(antecedent)])
    solver = Solver()
    solver.add(Not(Implies(lhs, rhs)))
    return solver.check() == unsat
