from dataclasses import dataclass, field
from uuid import uuid4, UUID
from typing import Union


Formula = Union['Left', 'Right', 'Constant', 'Variable', 'And', 'Or', 'Imply', 'Iff']


@dataclass(frozen=True)
class Left:
    fml: Formula

    def __repr__(self) -> str:
        fml = self.fml
        match self.fml:
            case Variable() | Constant():
                fml = str(self.fml)
            case _:
                fml = '(' + str(self.fml) + ')'
        return 'L ' + str(fml)


@dataclass(frozen=True)
class Right:
    fml: Formula

    def __repr__(self) -> str:
        fml = self.fml
        match self.fml:
            case Variable() | Constant():
                fml = str(self.fml)
            case _:
                fml = '(' + str(self.fml) + ')'
        return 'R ' + str(fml)


@dataclass(frozen=True)
class Constant:
    name: str

    def __repr__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Variable:
    uuid: UUID = field(default_factory=uuid4)

    def __repr__(self) -> str:
        return '$' + str(self.uuid)[:8]


@dataclass(frozen=True)
class And:
    lhs: Formula
    rhs: Formula

    def __repr__(self) -> str:
        lhs = str(self.lhs)
        match self.lhs:
            case Variable() | Constant():
                lhs = str(self.lhs)
            case _:
                lhs = '(' + lhs + ')'
        rhs = str(self.rhs)
        match self.rhs:
            case Variable() | Constant():
                rhs = str(self.rhs)
            case _:
                rhs = '(' + rhs + ')'
        return lhs + ' & ' + rhs


@dataclass(frozen=True)
class Or:
    lhs: Formula
    rhs: Formula

    def __repr__(self) -> str:
        lhs = str(self.lhs)
        match self.lhs:
            case Variable() | Constant():
                lhs = str(self.lhs)
            case _:
                lhs = '(' + lhs + ')'
        rhs = str(self.rhs)
        match self.rhs:
            case Variable() | Constant():
                rhs = str(self.rhs)
            case _:
                rhs = '(' + rhs + ')'
        return lhs + ' | ' + rhs


@dataclass(frozen=True)
class Imply:
    lhs: Formula
    rhs: Formula

    def __repr__(self) -> str:
        lhs = str(self.lhs)
        match self.lhs:
            case Variable() | Constant():
                lhs = str(self.lhs)
            case _:
                lhs = '(' + lhs + ')'
        rhs = str(self.rhs)
        match self.rhs:
            case Variable() | Constant():
                rhs = str(self.rhs)
            case _:
                rhs = '(' + rhs + ')'
        return lhs + ' -> ' + rhs


@dataclass(frozen=True)
class Iff:
    lhs: Formula
    rhs: Formula

    def __repr__(self) -> str:
        lhs = str(self.lhs)
        match self.lhs:
            case Variable() | Constant():
                lhs = str(self.lhs)
            case _:
                lhs = '(' + lhs + ')'
        rhs = str(self.rhs)
        match self.rhs:
            case Variable() | Constant():
                rhs = str(self.rhs)
            case _:
                rhs = '(' + rhs + ')'
        return lhs + ' <-> ' + rhs
