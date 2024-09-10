from dataclasses import dataclass


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
