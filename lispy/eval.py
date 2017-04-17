import math
import operator as op

from .primitives import (
    Symbol, List, Number,
    _quote, _if, _define, _set, _lambda
)


class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."

    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self:
            return self
        elif self.outer is not None:
            return self.outer.find(var)
        else:
            raise LookupError("'%s' is not defined" % var)


def standard_env():
    "An environment with some Scheme standard procedures."
    env = Env()
    env.update({
        name: fn
        for name, fn in vars(math).iteritems() if not name.startswith('__')
    })  # sin, cos, sqrt, pi, ...
    env.update({
        '+': op.add,
        '-': op.sub,
        '*': op.mul,
        '/': op.div,
        '>': op.gt,
        '<': op.lt,
        '>=': op.ge,
        '<=': op.le,
        '=': op.eq,
        'abs': abs,
        'append': op.add,
        'apply': apply,
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: List(x),
        'list?': lambda x: isinstance(x, List),
        'map': map,
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env


global_env = standard_env()


class Procedure(object):
    "A user-defined Scheme procedure."

    def __init__(self, parms, body, env):
        self.parms = parms
        self.body = body
        self.env = env

    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))


def eval(x, env=global_env):
    "Evaluate an expression in an environment."
    if isinstance(x, Symbol):      # variable reference
        return env.find(x)[x]
    elif not isinstance(x, List):  # constant literal
        return x
    elif x[0] is _quote:          # quotation
        (_, exp) = x
        return exp
    elif x[0] is _if:             # conditional
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] is _define:         # definition
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x[0] is _set:           # assignment
        (_, var, exp) = x
        env.find(var)[var] = eval(exp, env)
    elif x[0] is _lambda:         # procedure
        (_, parms, body) = x
        return Procedure(parms, body, env)
    else:                          # procedure call
        proc = eval(x[0], env)
        args = [eval(arg, env) for arg in x[1:]]
        return proc(*args)
