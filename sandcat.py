from abc import ABC, abstractmethod
from functools import reduce

from sympy import And, Expr, Implies, Not, Symbol, satisfiable  # type: ignore


class Category(ABC):
    def __lshift__(self, other: "Category") -> "Left":
        return Left(self, other)

    def __rshift__(self, other: "Category") -> "Right":
        return Right(self, other)

    @abstractmethod
    def __repr__(self) -> str:
        pass


class Left(Category):
    def __init__(self, lhs: Category, rhs: Category):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self) -> str:
        lhs = str(self.lhs)
        if isinstance(self.lhs, Left | Right):
            lhs = f"({lhs})"
        rhs = str(self.rhs)
        if isinstance(self.rhs, Left | Right):
            rhs = f"({rhs})"
        return f"{lhs} << {rhs}"


class Right(Category):
    def __init__(self, lhs: Category, rhs: Category):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self) -> str:
        rhs = str(self.rhs)
        if isinstance(self.rhs, Left | Right):
            rhs = f"({rhs})"
        lhs = str(self.lhs)
        if isinstance(self.lhs, Left | Right):
            lhs = f"({lhs})"
        return f"{lhs} >> {rhs}"


class Atom(Category):
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return self.name


def translate1(cat: Category, i: int) -> Expr:
    if isinstance(cat, Atom):
        return Symbol(f"{cat}{i}")
    elif isinstance(cat, Right):
        lhs = translate1(cat.lhs, i - 1)
        rhs = translate1(cat.rhs, i)
        return Implies(lhs, rhs)
    elif isinstance(cat, Left):
        lhs = translate1(cat.rhs, i + 1)
        rhs = translate1(cat.lhs, i)
        return Implies(lhs, rhs)


def translateN(cats: list[Category]) -> Expr:
    fml = [translate1(cats[i], i + 1) for i in range(len(cats))]
    lhs = reduce(And, fml)
    return lhs


def check(cats: list[Category], cat: Category) -> bool:
    lhs = translateN(cats)
    for i in range(1, len(cats)+1):
        if not satisfiable(Not(Implies(lhs, translate1(cat, i))), algorithm="z3"):
            return True
    return False


A, B, C = Atom("A"), Atom("B"), Atom("C")


# Example usage
print(f"{check([C << A, B, A], C)=}")
print(f"{check([C << A, A, B], C)=}")
print(f"{check([C << A, A, C >> C], C)=}")
