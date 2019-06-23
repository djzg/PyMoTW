#!/usr/bin/env/python3


""" operator - Functional interaface to built-in operators """


# The operator module defines functions that correspond to built-in operations for arithmetic, comparison and other
# operations corresponding to standard object APIs


""" Logical operations """

# There are functions for determining the boolean equivalent for a value, negating it to create the opposite boolean
# value, and comparing objects to see if they are identical.


from operator import *

a = -1
b = 5

print("a = ", a)
print("b = ", b)
print()

# not_() includes the trailing underscore because not is a Python keyword.
print("not_(a)      :", not_(a))
# truth() applies the same logic used when testing an expression in an if statement or converting an expression to bool.
print("truth(a)     :", truth(a))
# is_() implements the same check used by the is keyword
print("is_(a, b)    :", is_(a, b))
# is_not() does the same test and returns the opposite answer.
print("is_not(a, b) :", is_not(a, b))
print()

""" Comparison operators """

a = 10
b = 5.0

print("a = ", a)
print("b = ", b)
for func in (lt, le, eq, ne, ge, gt):
    print("{}(a, b): {}".format(func.__name__, func(a, b)))

print()

""" Arithmetic operators """

a = -1
b = 5.0
c = 2
d = 6

print('a =', a)
print('b =', b)
print('c =', c)
print('d =', d)

print("\nPositive/Negative:")
print("abs(a):", abs(a))
print("neg(a):", neg(a))
print("neg(b):", neg(b))
print("pos(a):", pos(a))
print("pos(b):", pos(b))

print("\nArithmetic:")
print("add(a, b)        :", add(a, b))
print("floordiv(a, b)   :", floordiv(a, b))
print("floordiv(d, c)   :", floordiv(d, c))
print("mod(a, b)        :", mod(a, b))
print("mul(a, b)        :", mul(a, b))
print("pow(c, d)        :", pow(c, d))
print("sub(c, a)        :", sub(c, a))
print("truediv(a, b)    :", truediv(a, b))
print("truediv(d, c)    :", truediv(d, c))

print("\nBitwise:")
print('and_(c, d)  :', and_(c, d))
print('invert(c)   :', invert(c))
print('lshift(c, d):', lshift(c, d))
print('or_(c, d)   :', or_(c, d))
print('rshift(d, c):', rshift(d, c))
print('xor(c, d)   :', xor(c, d))
print()

""" Sequence operators """


# The operators for working with sequences can be divided into four groups, building up sequences, searching for items,
# accessing contents, and removing items from sequences.

a = [1, 2, 3]
b = ["a", "b", "c"]

print("a=", a)
print("b=", b)

print("\nConstructive:")
print("     concat(a, b):", concat(a, b))

print("\nSearching:")
print(" contains(b, 'd'):", contains(b, "d"))
print("    countOf(a, 1):", countOf(a, 1))
print("  countOf(b, 'd'):", countOf(b, "d"))
print("    indexOf(a, 1):", indexOf(a, 1))

print("\nAccess items:")
print("getitem(b, 1)                  :", getitem(b, 1))
print("getitem(b, slice(1, 3))        :", getitem(b, slice(1, 3)))
print("setitem(b, 1, 'd')             :", end=" ")
setitem(b, 1, 'd')
print(b)
print("setitem(a, slice(1, 3), [4, 5]):", end=" ")
setitem(a, slice(1, 3), [4, 5])
print(a)

print("\nDestructive:")
print("delitem(b, 1)         :", end=" ")
delitem(b, 1)
print(b)
print("delitem(a, slice(1, 3):", end=" ")
delitem(a, slice(1, 3))
print(a)
# Some of these operations, such as setitem() and delitem(), modify the sequence in place and do not return a value.
print()

""" In-place operators """

# In addition to the standard operators, many types of objects support "in-place" modification through special operators
# such as +=. There are equivalent functions for in-place modifications, too.

a = -1
b = 5.0
c = [1, 2, 3]
d = ["a", "b", "c"]

print('a =', a)
print('b =', b)
print('c =', c)
print('d =', d)
print()

a = iadd(a, b)
print("a = iadd(a, b) =>", a)
print()

c = iconcat(c, d)
print("c = iconcat(c, d) =>", c)


""" Attribute and item "getters" """

# Getters are callable objects constructed at runtime to retrieve attributes of objects or contents from sequences.
# They are especially useful when working with iterators or generator sequences, where they are intended to incur less
# overhead than a lambda or Python function


class MyObj:
    "Example class for attrgetter"

    def __init__(self, arg):
        super().__init__()
        self.arg = arg

    def __repr__(self):
        return "MyObj({})".format(self.arg)


l = [MyObj(i) for i in range(5)]
print("objects  :", l)

# Extract the "arg" value from each object
g = attrgetter("arg")
vals = [g(i) for i in l]
print("arg values:", vals)

# Sort using arg
l.reverse()
print("reversed :", l)
print("sorted   :", sorted(l, key=g))
# Attribute getters work like lambda x, n="attrname": getattr(x, n)
print()
# Item getters work like lambda x, y=5: x[y]

l = [dict(val =-1 * i) for i in range(4)]
print("Dictionaries:")
print(" orginal:", l)
g = itemgetter("val")
vals = [g(i) for i in l]
print(" values :", vals)
print(" sorted :", sorted(l, key=g))

print()
l = [(i, i * -2) for i in range(4)]
print("\nTuples:")
print(" original:", l)
g = itemgetter(l)
vals = [g(i) for i in l]
print(" values  :", vals)
print(" sorted  :", sorted(l, key=g))


""" Combining operators and custom classes """



class MyObj:
    """Example for operator overloading"""

    def __init__(self, val):
        super(MyObj, self).__init__()
        self.val = val

    def __str__(self):
        return 'MyObj({})'.format(self.val)

    def __lt__(self, other):
        """compare for less-than"""
        print('Testing {} < {}'.format(self, other))
        return self.val < other.val

    def __add__(self, other):
        """add values"""
        print('Adding {} + {}'.format(self, other))
        return MyObj(self.val + other.val)


a = MyObj(1)
b = MyObj(2)

print('Comparison:')
print(lt(a, b))

print('\nArithmetic:')
print(add(a, b))