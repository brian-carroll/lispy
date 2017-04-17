# Basic LISP primitives
# Imported by lots of modules. Should have as few imports as possible.

# tuple arg to 'isinstance' checks for ANY of the classes
Number = (int, float)
List = list


class Symbol(str):
    pass


def Sym(s, symbol_table={}):
    "Find or create unique Symbol entry for str s in symbol table."
    if s not in symbol_table:
        symbol_table[s] = Symbol(s)
    return symbol_table[s]


_quote, _if, _set, _define, _lambda, _begin, _definemacro, = map(
    Sym,
    "quote   if   set!  define   lambda   begin   define-macro".split())

_quasiquote, _unquote, _unquotesplicing = map(
    Sym,
    "quasiquote   unquote   unquote-splicing".split())

quotes = {
    "'": _quote,
    "`": _quasiquote,
    ",": _unquote,
    ",@": _unquotesplicing
}

eof_object = Symbol('#<eof-object>')  # Note: uninterned; can't be read
