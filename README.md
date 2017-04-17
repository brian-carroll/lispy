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
