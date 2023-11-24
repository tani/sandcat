from dataclasses import dataclass, field
from uuid import uuid4, UUID
from typing import Union


Category = Union['Unbound', 'Atom', 'Right', 'Left']


@dataclass(frozen=True)
class Unbound:
    uuid: UUID = field(default_factory=uuid4)

    def __repr__(self) -> str:
        return '$' + str(self.uuid)[:8]

    def __lt__(self, other: Category) -> 'Left':
        return Left(arg=other, ret=self)  # self < other

    def __gt__(self, other: Category) -> 'Right':
        return Right(arg=self, ret=other)  # self > other


@dataclass(frozen=True)
class Atom:
    name: str

    def __repr__(self) -> str:
        return self.name

    def __lt__(self, other: Category) -> 'Left':
        return Left(arg=other, ret=self)  # self < other

    def __gt__(self, other: Category) -> 'Right':
        return Right(arg=self, ret=other)  # self > other


@dataclass(frozen=True)
class Right:
    arg: Category
    ret: Category

    def __repr__(self) -> str:
        ret = str(self.ret)
        match self.ret:
            case Left() | Right():
                ret = '(' + ret + ')'
        arg = str(self.arg)
        match self.arg:
            case Left() | Right():
                arg = '(' + arg + ')'
        return arg + ' > ' + ret

    def __lt__(self, other: Category) -> 'Left':
        return Left(arg=other, ret=self)  # self < other

    def __gt__(self, other: Category) -> 'Right':
        return Right(arg=self, ret=other)  # self > other


@dataclass(frozen=True)
class Left:
    arg: Category
    ret: Category

    def __repr__(self) -> str:
        ret = str(self.ret)
        match self.ret:
            case Left() | Right():
                ret = '(' + ret + ')'
        arg = str(self.arg)
        match self.arg:
            case Left() | Right():
                arg = '(' + arg + ')'
        return ret + ' < ' + arg

    def __lt__(self, other: Category) -> 'Left':
        return Left(arg=other, ret=self)  # self < other

    def __gt__(self, other: Category) -> 'Right':
        return Right(arg=self, ret=other)  # self > other


