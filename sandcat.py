from dataclasses import dataclass
from typing import Unpack

from sympy import And, Expr, Implies, Not, Or, SatOpts, Symbol, satisfiable


@dataclass(frozen=True)
class Atom:
    name: str

    def __lshift__(self, other: "Category") -> "Category":
        return Left(self, other)

    def __rshift__(self, other: "Category") -> "Category":
        return Right(self, other)

    def __repr__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Left:
    lhs: "Category"
    rhs: "Category"

    def __lshift__(self, other: "Category") -> "Category":
        return Left(self, other)

    def __rshift__(self, other: "Category") -> "Category":
        return Right(self, other)

    def __repr__(self) -> str:
        lhs = f"{self.lhs}" if isinstance(self.lhs, Atom) else f"({self.lhs})"
        rhs = f"{self.rhs}" if isinstance(self.rhs, Atom) else f"({self.rhs})"
        return f"{lhs} << {rhs}"


@dataclass(frozen=True)
class Right:
    lhs: "Category"
    rhs: "Category"

    def __lshift__(self, other: "Category") -> "Category":
        return Left(self, other)

    def __rshift__(self, other: "Category") -> "Category":
        return Right(self, other)

    def __repr__(self) -> str:
        lhs = f"{self.lhs}" if isinstance(self.lhs, Atom) else f"({self.lhs})"
        rhs = f"{self.rhs}" if isinstance(self.rhs, Atom) else f"({self.rhs})"
        return f"{lhs} >> {rhs}"


Category = Atom | Left | Right


def translate(i: int, cat: Category) -> Expr:
    match cat:
        case Atom(name):
            return Symbol(f"{name}{i}")
        case Left(lhs, rhs):
            return Implies(translate(i + 1, rhs), translate(i, lhs))
        case Right(lhs, rhs):
            return Implies(translate(i - 1, lhs), translate(i, rhs))


def check(cats: list[Category], cat: Category, **kwargs: Unpack[SatOpts]) -> bool:
    lhs = And(*[translate(i, cat) for (i, cat) in enumerate(cats)])
    rhs = Or(*[translate(i, cat) for i in range(len(cats))])
    return not satisfiable(Not(Implies(lhs, rhs)), **kwargs)
