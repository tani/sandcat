from abc import ABC, abstractmethod
from functools import reduce
from typing import override
from sympy import Symbol, Expr, satisfiable


class Category(ABC):
    def __lshift__(self, other: "Category") -> "Left":
        return Left(self, other)

    def __rshift__(self, other: "Category") -> "Right":
        return Right(self, other)

    @override
    @abstractmethod
    def __repr__(self) -> str:
        pass


class Left(Category):
    def __init__(self, lhs: Category, rhs: Category):
        self.lhs = lhs
        self.rhs = rhs

    @override
    def __repr__(self) -> str:
        lhs = str(self.lhs)
        if isinstance(self.lhs, (Left, Right)):
            lhs = f"({lhs})"
        rhs = str(self.rhs)
        if isinstance(self.rhs, (Left, Right)):
            rhs = f"({rhs})"
        return f"{lhs} << {rhs}"


class Right(Category):
    def __init__(self, lhs: Category, rhs: Category):
        self.lhs = lhs
        self.rhs = rhs

    @override
    def __repr__(self) -> str:
        rhs = str(self.rhs)
        if isinstance(self.rhs, (Left, Right)):
            rhs = f"({rhs})"
        lhs = str(self.lhs)
        if isinstance(self.lhs, (Left, Right)):
            lhs = f"({lhs})"
        return f"{lhs} >> {rhs}"


class Atom(Category):
    def __init__(self, name: str):
        self.name = name

    @override
    def __repr__(self) -> str:
        return self.name


def translate1(cat: Category, i: int) -> Expr:
    if isinstance(cat, Atom):
        return Symbol(f"{i}") >> Symbol(str(cat))
    elif isinstance(cat, Right):
        lhs = translate1(cat.lhs, i - 1)
        rhs = translate1(cat.rhs, i)
        return lhs >> rhs
    elif isinstance(cat, Left):
        lhs = translate1(cat.rhs, i + 1)
        rhs = translate1(cat.lhs, i)
        return lhs >> rhs


def translateN(cats: list[Category]) -> Expr:
    fml = [translate1(cats[i], i + 1) for i in range(len(cats))]
    lhs = reduce(lambda x, y: x & y, fml)
    return lhs


def check(cats: list[Category], cat: Category) -> bool:
    lhs = translateN(cats)
    for i in range(1, len(cats)+1):
        if not satisfiable(~ (lhs >> translate1(cat, i))):
            return True
    return False


A, B, C = Atom("A"), Atom("B"), Atom("C")


# Example usage
# print(check([C << A, B, A], C))
# print(check([C << A, A, B], C))
# print(check([C << A, A, C >> C], C))

