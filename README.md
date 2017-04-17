Lispy
=====
A Lisp (Scheme) interpreter implemented in Python

Based on [this tutorial](http://norvig.com/lispy.html)

Interesting to compare to [my previous Scheme interpreter](https://github.com/brian-carroll/haskell-simple-compiler)
which was implemented in Haskell.
Haskell version is more complicated due to monads. (It's a cliche but it's true!)
But Haskell pattern matching is nice, and refactoring was great.
Python version feels more loose, e.g. defining Number as a tuple instead of a class, just because isinstance accepts tuples, feels like an awkward special case.
Python tokenizer uses regex which is disgusting compared to Haskell's parsec.


Code organisation
-----------------
Let's clean this up. Tutorial doesn't split things into files but I want to!

- Parsing
    - Deals with:
        - File stuff and parsing stuff (mixed together)
            - All input is from a file via port (maybe stdin)
            - Ports yield tokens
            - 'read' yields expressions (as AST datastructures)
                - Has knowledge of quotes, some syntax (quotes, atoms)
        - Macro expansion & syntax checking
    - Should contain:
        - load
        - eof_object
        - readchar
        - read
        - atom
        - parse
        - build_tokenizer
        - InPort

- AST (imported into parsing and eval)
    - Should contain:
        - Number
        - list
        - Symbol

- Evaluation
    - Deals with:
        - Environment
        - Primitive/builtin functions
            - quotes
            - lambda, define, if...
            - math stuff
    - Should contain:
        - standard_env
        - Procedure
        - Env
        - global_env
        - eval

- REPL
    - Should contain:
        - to_string
        - repl
        - schemestr

- CLI
    - probably want some top-level executable file
