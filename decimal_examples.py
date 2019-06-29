#!/usr/bin/env/python3

""" decimal - Fixed and Floating point math """

# The decimal module implements fixed and floating point arithmetic using the model familiar to most people.
# A Decimal instance can represent any number exactly, round up or down, and apply a limit to the number of significant
# digits.

""" Decimal """

# Decimal values are represented as instance of the Decimal class. The constructor takes as argument one integer or
# string. Floating point numbers can be converted to a string before being used to create a Decimal, letting the caller
# explicitly deal with the number of digits for values that cannot be expressed exactly using hardware floating point
# representations. Alternately, the class method from_float() converts to the exact decimal representation.

import decimal

fmt = "{0:<25} {1:<25}"

print(fmt.format("Input", "Output"))
print(fmt.format("-" * 25, "-" * 25))

# Integer
print(fmt.format(5, decimal.Decimal(5)))

# String
print(fmt.format("3.14", decimal.Decimal("3.14")))

# Float
f = 0.1
print(fmt.format(repr(f), decimal.Decimal(str(f))))
print("{:<0.23g} {:<25}".format(
    f,
    str(decimal.Decimal.from_float(f))[:25])
)

# The floating point value of 0.1 is not represented as an exact value in binary, so the representation as a float is
# different from the Decimal value. The full string representation is truncated to 25 characters in the last line of
# this output.

# Decimals can also be created from tuples containing a sign flag (0 for positive, 1 for negative), a tuple of digits,
# and an integer exponent.

# Tuple
t = (1, (1, 1), -2)
print("Input:", t)
print("Decimal:", decimal.Decimal(t))
print()

# The tuple-based representation is less convenient to create, but does offer a portable way of exporting decimal values
# without losing precision. The tuple form can be transmitted through the network or stored in a database that does not
# support accurate decimal values, the nturned back into a Decimal instance later.


""" Formatting """

# Decimal responts to Python's string formatting protocol, using the same syntax and options as other numerical types.

d = decimal.Decimal(1.1)
print("Precision:")
print("{:.1}".format(d))
print("{:.2}".format(d))
print("{:.3}".format(d))
print("{:.18}".format(d))

print("\nWidth and precision combined:")
print("{:5.1f} {:5.1g}".format(d, d))
print("{:5.2f} {:5.2g}".format(d, d))
print("{:5.3f} {:5.3g}".format(d, d))

print("\nZero padding:")
print("{:05.1}".format(d, d))
print("{:05.2}".format(d, d))
print("{:05.3}".format(d, d))

# The format strings can control the width of the output, the precision (number of significant digits), and how to pad
# the value to fill the width.


""" Arithmetic """

# Decimal overloads the simple arithmetic operators so instances can be manipulated in much the same way as the
# built-in numeric types

a = decimal.Decimal("5.1")
b = decimal.Decimal("3.14")
c = 4
d = 3.14

print("a = ", repr(a))
print("b = ", repr(b))
print("c = ", repr(c))
print("d = ", repr(d))
print()

print("a + b = ", a + b)
print("a - b = ", a - b)
print("a * b = ", a * b)
print("a / b = ", a / b)
print()

print("a + c = ", a + c)
print("a - c = ", a - c)
print("a * c = ", a * c)
print("a / c = ", a / c)
print()

print("a + d = ", end=" ")
try:
    print(a + d)
except TypeError as e:
    print(e)

# Decimal operators also accept integer arguments, but floating point values must be converted to Decimal instances.


""" Special values """

# In addition to the expected numerical values, Decimal can represent several special values, including positive and
# negative values for infinity, "not a number", and zero.

for value in ["Infinity", "NaN", "0"]:
    print(decimal.Decimal(value), decimal.Decimal("-" + value))
print()

# Math with infinity
print("Infinity + 1:", (decimal.Decimal("Infinity") + 1))
print("-Infinity + 1:", (decimal.Decimal("-Infinity") + 1))

# Print comparing NaN
print(decimal.Decimal("NaN") == decimal.Decimal("Infinity"))
print(decimal.Decimal("NaN") != decimal.Decimal(1))

# Adding to infinite values returns another infinite values. Comparing for equality with NaN always returns false and
# comparing for inequality always returns true. Comparing for sort order against NaN is undefined and results in error.


""" Context """

# It is possible to override settings such as the precision maintained, how rounding is performed, error handling, etc
# by using a context. Contexts can be applied for all Decimal instances in a thread or locally within a small code region

context = decimal.getcontext()

print("Emax         = ", context.Emax)
print("Emin         = ", context.Emin)
print("capitals     = ", context.capitals)
print("prec         = ", context.prec)
print("rounding     = ", context.rounding)
print("flags        = ", context.flags)

for f, v in context.flags.items():
    print(" {}: {}".format(f, v))
print("traps        =")
for t, v in context.traps.items():
    print(" {}: {}".format(t, v))

# This example script shows the public properties of a Context


""" Precision """

# The prec attribute of the context controls the precision maintained for new values created as a result of arithmetic.

d = decimal.Decimal("0.123456")

for i in range(1, 5):
    decimal.getcontext().prec = i
    print(i, ":", d, d * i)
print()
# To change the precision, assign a new value between 1 and decimal.MAX_PREC directly to the attribute


""" Rounding """

# There are several options for rounding to keep values within the desired precision.

context = decimal.getcontext()

ROUNDING_MODES = [
    "ROUND_CEILING",
    "ROUND_DOWN",
    "ROUND_FLOOR",
    "ROUND_HALF_DOWN",
    "ROUND_HALF_EVEN",
    "ROUND_HALF_UP",
    "ROUND_UP",
    "ROUND_05UP",
]

header_fmt = " {:10} " + " ".join(["{:^8}"] * 6)

print(header_fmt.format(
    " ",
    "1/8 (1)", "-1/8 (1)",
    "1/8 (2)", "-1/8 (2)",
    "1/8 (3)", "-1/8 (3)",
))

for rounding_mode in ROUNDING_MODES:
    print("{0:10}".format(rounding_mode.partition("_")[-1]), end=" ")
    for precision in [1, 2, 3]:
        context.prec = precision
        context.rounding = getattr(decimal, rounding_mode)
        value = decimal.Decimal(1) / decimal.Decimal(8)
        print("{0:^8}".format(value), end=" ")
        value = decimal.Decimal(-1) / decimal.Decimal(8)
        print("{0:^8}".format(value), end=" ")
    print()
print()

# This program shows the effect of rounding the same value to different levels of precision using the different algorithms.


""" Local context """

# The context can be applied to a block of code using the "with" statement

with decimal.localcontext() as c:
    c.prec = 2
    print("Local precision:", c.prec)
    print("3.14 / 3 =", (decimal.Decimal("3.14") / 3))

print()
print("Default precision:", decimal.getcontext().prec)
print("3.14 / 3 = ", (decimal.Decimal("3.14") / 3))


""" Per-instance context """

# Context also can be used to construct Decimal instances, which then inherit the precision and rounding arguments to
# the conversion from the context.d


# setup a context with limited precision
c = decimal.getcontext().copy()
c.prec = 3

# create our constant
pi = c.create_decimal("3.12345")

# the constant value is rounded off
print("PI:", pi)

# the result of using the constant uses the global context
print("RESULT:", decimal.Decimal("2.01") * pi)
print()

# This lets an application select the precision of constant values separately from the precision of user data.


""" Threads """

# The "global" context is actually thread-local, so each thread can potentially be configured using different values.

import threading
from queue import PriorityQueue


class Multiplier(threading.Thread):
    def __init__(self, a, b, prec, q):
        self.a = a
        self.b = b
        self.prec = prec
        self.q = q
        threading.Thread.__init__(self)

    def run(self):
        c = decimal.getcontext().copy()
        c.prec = self.prec
        decimal.setcontext(c)
        self.q.put((self.prec, a * b))


a = decimal.Decimal("3.14")
b = decimal.Decimal("1.234")

# a PriorityQueue will return values sorted by precision, no matter what order the threads finish
q = PriorityQueue()
threads = [Multiplier(a, b, i, q) for i in range(1, 6)]
for t in threads:
    t.start()

for t in threads:
    t.join()

for i in range(5):
    prec, value = q.get()
    print("{} {}".format(prec, value))

# This example creates a new context using the specified, then installs it within each thread.

