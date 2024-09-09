from dataclasses import dataclass

from sympy import And, Expr, Implies, Not, Or, Symbol, satisfiable  # type: ignore


class Category:
    def __lshift__(self, other: "Category") -> "Left":
        return Left(self, other)

    def __rshift__(self, other: "Category") -> "Right":
        return Right(self, other)


@dataclass(frozen=True)
class Left(Category):
    lhs: Category
    rhs: Category

    def __repr__(self) -> str:
        lhs = str(self.lhs)
        if isinstance(self.lhs, Left | Right):
            lhs = f"({lhs})"
        rhs = str(self.rhs)
        if isinstance(self.rhs, Left | Right):
            rhs = f"({rhs})"
        return f"{lhs} << {rhs}"


@dataclass(frozen=True)
class Right(Category):
    lhs: Category
    rhs: Category

    def __repr__(self) -> str:
        rhs = str(self.rhs)
        if isinstance(self.rhs, Left | Right):
            rhs = f"({rhs})"
        lhs = str(self.lhs)
        if isinstance(self.lhs, Left | Right):
            lhs = f"({lhs})"
        return f"{lhs} >> {rhs}"


@dataclass(frozen=True)
class Atom(Category):
    name: str

    def __repr__(self) -> str:
        return self.name


def translate(i: int, cat: Category) -> Expr:
    if isinstance(cat, Atom):
        return Symbol(f"{cat}{i}")
    elif isinstance(cat, Right):
        lhs = translate(i - 1, cat.lhs)
        rhs = translate(i, cat.rhs)
        return Implies(lhs, rhs)
    elif isinstance(cat, Left):
        lhs = translate(i + 1, cat.rhs)
        rhs = translate(i, cat.lhs)
        return Implies(lhs, rhs)


def check(cats: list[Category], cat: Category, **kwargs) -> bool:
    lhs = And(*[translate(i, cat) for (i, cat) in enumerate(cats)])
    rhs = Or(*[translate(i, cat) for i in range(len(cats))])
    return not satisfiable(Not(Implies(lhs, rhs)), **kwargs)
