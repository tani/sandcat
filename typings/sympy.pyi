# sympy_stub.pyi
from typing import Literal, TypedDict, Unpack

class Expr: ...

class Symbol(Expr):
    def __init__(self, name: str) -> None: ...

class And(Expr):
    def __init__(self, *args: Expr) -> None: ...

class Or(Expr):
    def __init__(self, *args: Expr) -> None: ...

class Not(Expr):
    def __init__(self, arg: Expr) -> None: ...

class Implies(Expr):
    def __init__(self, lhs: Expr, rhs: Expr) -> None: ...

class SatOpts(TypedDict):
    algorithms: Literal["z3", "minisat22", "dpll2", "dpll", "pycosat"] | None
    #all_models: bool
    minimal: bool
    use_lra_theory: bool

SatRetval = Literal[False] | dict[Symbol, bool]

def satisfiable(expr: Expr, **kwargs: Unpack[SatOpts]) -> SatRetval: ...
