import sys

from .primitives import Symbol
from .parser import read, InPort, eof_object
from .eval import eval


def to_string(x):
    "Convert a Python object back into a Lisp-readable string."
    if x is True:
        return "#t"
    elif x is False:
        return "#f"
    elif isinstance(x, Symbol):
        return x
    elif isinstance(x, str):
        return '"%s"' % x.encode('string_escape').replace('"', r'\"')
    elif isinstance(x, list):
        return '(' + ' '.join(map(to_string, x)) + ')'
    elif isinstance(x, complex):
        return str(x).replace('j', 'i')
    else:
        return str(x)


def repl(prompt='lispy> ', inport=InPort(sys.stdin), out=sys.stdout):
    "A prompt-read-eval-print loop."
    sys.stderr.write("Lispy version 2.0\n")
    while True:
        try:
            if prompt:
                sys.stderr.write(prompt)
            x = read(inport)
            if x is eof_object:
                return
            val = eval(x)
            if val is not None and out:
                print >> out, to_string(val)
        except Exception as e:
            print '%s: %s' % (type(e).__name__, e)


def load(filename):
    "Eval every expression from a file."
    with open(filename) as f:
        repl(prompt=None, inport=InPort(f))  # , out=None)
