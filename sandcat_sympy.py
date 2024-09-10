from sympy import And, Expr, Implies, Not, Or, Symbol, satisfiable

from category import Atom, Category, Left, Right


def translate(i: int, cat: Category) -> Expr:
    match cat:
        case Atom(name):
            return Symbol(f"{name}{i}")
        case Left(lhs, rhs):
            return Implies(translate(i + 1, rhs), translate(i, lhs))
        case Right(lhs, rhs):
            return Implies(translate(i - 1, lhs), translate(i, rhs))


def check(antecedent: list[Category], succedent: Category) -> bool:
    lhs = And(*[translate(i, cat) for (i, cat) in enumerate(antecedent)])
    rhs = Or(*[translate(i, succedent) for (i, _) in enumerate(antecedent)])
    return not satisfiable(Not(Implies(lhs, rhs)))
