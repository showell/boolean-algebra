This repo contains small Python modules that are mostly intended
for instructional use. I have no immediate intentions of creating
a package, but if you want to use any of the code, it is all in
the [public domain](LICENSE). I recommend the strategy of simply
pulling files directly into your own project.

## Basic booleans ##

The [basic_bool.py](./basic_bool.py) module is a finished product
that allows you to Pythonically build an [AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree)
for a boolean expression.  It is less than 100 lines of code.

Its construction API is basically `TRUE`, `FALSE`, and `SYMBOL`,
and then you can build up larger expressions using code like
`x & y`, `a | b`, and `~z`.

Then the objects themselves allow the following:

<pre>
    x = SYMBOL("x")
    y = SYMBOL("y")

    str(~y | x) == "(~y)|(x)"
    (~y | x).symbols() == {"x", "y"}
    (x | y).eval({"x", "y")) == True
    (~x).eval({"x")) == False
    (y).eval({"x")) == False
</pre>

The code is very reliable due to its simplicity, and you can read
[test_basic.py](./test_basic.py) to see its basic operation.

The code has no optimizations, but the performance should be fine
for most use cases.  (When you evaluate AND and OR pairs, Python
can get lucky and be able to avoid traversing the second
subtree.)

## Boolean "solver" ##

The [solver.py](./solver.py) module is a super-tiny module that finds
all satisfying variable assignments for a boolean expression.  It does
this completely by brute force, and the underlying code is equivalent
to just building out a truth table.  This code is mostly intended for
testing.

## Other stuff ##

Everything else is still in progress. (I am building code to simplify
boolean expressions.)

## Forking and packaging ##

If you have interest in turning some of this code into a package, then
please feel free to fork it. The licence puts you under no obligation
to give me credit, but I would be grateful for a short mention in a
readme file.  Thanks!
