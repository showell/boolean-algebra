## Basic booleans ##

The [basic_bool.py](./basic_bool.py) module is a finished product
that very simply represents an [AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree)
for a boolean expression.  It is less than 100 lines of code.

It has no optimizations, but unless you are evaluating monstrously large
boolean expressions, the performance should be fine.  (When you evaluate AND
and OR pairs, Python can get lucky and be able to avoid traversing the second
subtree.)

It is very reliable due to its simplicity, and you can read
[test_basic.py](./test_basic.py) to see its basic operation.

## Other stuff ##

Everything else is still in progress. (I am building code to simplify
boolean expressions.)
