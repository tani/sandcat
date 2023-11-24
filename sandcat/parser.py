from functools import reduce, cache
from typing import Callable, TypeGuard, Any
import z3 as z
import sandcat.category as c
import sandcat.formula as f


@cache
def translate(cat: c.Category) -> f.Formula:
    if isinstance(cat, c.Unbound):
        return f.Variable(cat.uuid)
    elif isinstance(cat, c.Atom):
        return f.Constant(cat.name)
    elif isinstance(cat, c.Right):
        return f.Imply(f.Left(translate(cat.arg)), f.Right(translate(cat.ret)))
    elif isinstance(cat, c.Left):
        return f.Imply(f.Right(translate(cat.arg)), f.Left(translate(cat.ret)))

#
# Provable A |- B, iff Valid A |= B, iff Unsat A & ~B
#
    

def parse(cats: list[c.Category]) -> f.Formula:
    @cache
    def parse_(start: int, end: int) -> tuple[list[f.Formula], list[f.Formula]]:
        if end - start == 1:
            return [f.Constant('Top')], [translate(cats[start])]
        else:
            assms: list[f.Formula] = []
            concs: list[f.Formula] = []
            for i in range(start + 1, end):
                lassms, lconcs = parse_(start, i)
                rassms, rconcs = parse_(i, end)
                for lassm, lconc in zip(lassms, lconcs):
                    for rassm, rconc in zip(rassms, rconcs):
                        conc = f.Variable()
                        concs.append(conc)
                        assm0 = f.Imply(f.And(f.Left(lconc), rconc), f.Right(conc))
                        assm1 = f.Imply(f.And(lconc, f.Right(rconc)), f.Left(conc))
                        assms.append(reduce(f.And, [lassm, rassm, f.Or(assm0, assm1)]))
            return assms, concs
    assms, concs = parse_(0, len(cats))
    # sents = map(lambda conc: f.Iff(conc, f.Constant('S')), concs)
    # sents = []
    # formulas: list[f.Formula] = []
    # for assm, sent in zip(assms, sents):
    #     formulas.append(f.And(assm, sent))
    return reduce(f.Or, assms)


def is_bool_ref(expr: Any) -> TypeGuard[z.BoolRef]:
    return isinstance(expr, z.BoolRef)


L = z.Function('L', z.BoolSort(), z.BoolSort())
R = z.Function('R', z.BoolSort(), z.BoolSort())


@cache
def calculate(formula: f.Formula) -> z.BoolRef:
    if isinstance(formula, f.Constant):
        if formula.name == 'Top':
            return z.BoolVal(True)
        else:
            return z.Bool(formula.name)
    elif isinstance(formula, f.Variable):
        return z.Bool(str(formula.uuid))
    elif isinstance(formula, f.Left):
        expr = L(calculate(formula.fml))
        if not is_bool_ref(expr):
            raise Exception(f'{formula} is not a BoolRef')
        return expr
    elif isinstance(formula, f.Right):
        expr = R(calculate(formula.fml))
        if not is_bool_ref(expr):
            raise Exception(f'{formula} is not a BoolRef')
        return expr
    elif isinstance(formula, f.Imply):
        return z.Implies(calculate(formula.lhs), calculate(formula.rhs))
    elif isinstance(formula, f.And):
        expr = z.And(calculate(formula.lhs), calculate(formula.rhs))
        if not is_bool_ref(expr):
            raise Exception(f'{formula} is not a BoolRef')
        return expr
    elif isinstance(formula, f.Or):
        expr = z.Or(calculate(formula.lhs), calculate(formula.rhs))
        if not is_bool_ref(expr):
            raise Exception(f'{formula} is not a BoolRef')
        return expr
    elif isinstance(formula, f.Iff):
        expr = z.And(
            z.Implies(calculate(formula.lhs), calculate(formula.rhs)),
            z.Implies(calculate(formula.rhs), calculate(formula.lhs))
        )
        if not is_bool_ref(expr):
            raise Exception(f'{formula} is not a BoolRef')
        return expr


def simplify(expr: z.BoolRef) -> z.BoolRef:
    expr = z.simplify(expr)
    if not is_bool_ref(expr):
        raise Exception(f'{expr} is not a BoolRef')
    return expr
    

def solve(expr: z.BoolRef) -> bool:
    solver = z.Solver()
    solver.add(z.Not(expr))
    return solver.check() == z.unsat


def pipe(value: Any, *funcs: Callable[[Any], Any]) -> Any:
    for func in funcs:
        value = func(value)
    return value


S = c.Atom('S')
A = c.Atom('A')
B = c.Atom('B')
C = c.Atom('C')
