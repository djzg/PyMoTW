#!/usr/bin/env/python3


""" functools - Tools for manipulating functions """

# The functools module provides tools for adapting or extending functions and other callable objects, without completely
# rewriting them.


""" Decorators """

# The primary tool supplied by this module is the class partial, which can be used to wrap a callable object with
# default arguments. The resulting object is itself callable and can be treated as though it is the original function.
# It takes all of the same arguments as the original, and can be invoked with extra positional or named arguments as well.
# A partical can be used instead of a lambda to provide default arugments to a function, while leaving some arguments
# unspecified


""" Partial objects """

# This example shows two simple partial objects for the function myfunc(). The output of show_details() includes
# the func, args, and keywords attributes of the partial object.

import functools


def myfunc(a, b=2):
    "Docstring for myfunc()."
    print(" called myfunc with:", (a, b))


def show_details(name, f, is_partial=False):
    "Show details of a callable object."
    print("{}:".format(name))
    print(" object:", f)
    if not is_partial:
        print(" __name__:", f.__name__)

    if is_partial:
        print("     func:", f.func)
        print("     args:", f.args)
        print(" keywords:", f.keywords)
    return


show_details("myfunc", myfunc)
myfunc("a", 3)
print()

# Set a different default value for "b", but require the caller to provide "a"
p1 = functools.partial(myfunc, b=4)
show_details("partial with named default", p1, True)
p1("passing a")
p1("override b", b=5)
print()

# Set default values for both "a" and "b"
p2 = functools.partial(myfunc, "default a", b=99)
show_details("partial with defaults", p2, True)
p2()
p2(b="override b")
print()

print("Insufficient arguments:")
try:
    p1()
except TypeError:
    print("TYPEERROR!: myfunc() missing 1 required positional argument: 'a' ")

print()

""" Acquiring function properties """

# The partial object does not have __name__ or __doc__ attributes by default, and without those attributes, decorated
# functions are more difficult to debug. Using update_wrapper(), copies or adds attributes from the original function
# to the partial object


def myfunc(a, b=2):
    "Docstring for myfunc()."
    print("     called myfunc with:", (a, b))


def show_details(name, f):
    "Show details of a callable object."
    print("{}:".format(name))
    print(" object:", f)
    print(" __name__:", end=" ")
    try:
        print(f.__name__)
    except AttributeError:
        print("no __name__")

    print(" __doc__", repr(f.__doc__))
    print()


show_details("myfunc", myfunc)

p1 = functools.partial(myfunc, b=4)
show_details("raw wrapper", p1)

print("Updating wrapper:")
# The attributes added to the wrapper are defined in WRAPPER_ASSIGNMENTS, while WRAPPER_UPDATES list values to be
# modified.
print("     assign:", functools.WRAPPER_ASSIGNMENTS)
print("     update:", functools.WRAPPER_UPDATES)
print()

functools.update_wrapper(p1, myfunc)
show_details("updated wrapper:", p1)


""" Other callables """

# Partials work with any callable object, just not with standalone functions


class MyClass:
    "Demonstration class for functools"

    def __call__(self, e, f=6):
        "Docstring for MyClass.__call__"
        print(" called object with:", (self, e, f))


def show_details(name, f):
    "Show details of a callable object."
    print("{}".format(name))
    print(" object:", f)
    print(" __name__:", end=" ")
    try:
        print(f.__name__)
    except AttributeError:
        print("no __name__")

    print(" __doc__", repr(f.__doc__))
    return

o = MyClass()

show_details("instance:", o)
o("e goes here")
print()

p = functools.partial(o, e="default for e", f=8)
functools.update_wrapper(p, o)
show_details("instance wrapper:", p)


""" Methods and functions """

# While partial() returns a callable ready to be used directly, partialmethod() returns a callable ready to be used as
# an unbound method of an object. In the following example, the same standalone function is added as an attribute of
# MyClass twice, once using partialmethod() as method1() and again using partial() as method2().

def standalone(self, a=1, b=2):
    "Standalone function"
    print(" called standalone with:", (self, a, b))
    if self is not None:
        print(" self.attr = ", self.attr)


class MyClass:
    "Demonstration class for functools"

    def __init__(self):
        self.attr = "instance attribute"

    method1 = functools.partialmethod(standalone)
    method2 = functools.partial(standalone)

o = MyClass()

print("standalone")
standalone(None)
print()

print("method1 as partialmethod")
o.method1()
print()

print("method2 as partial")
try:
    o.method2()
except TypeError as err:
    print("ERROR: {}".format(err))

print("-----")

""" Acquiring function properties for decorators """

# Updating the properties of a wrapped callable is especially useful when used in a decorator, since the transformed
# function ends up with properties of the original "bare" function


def show_details(name, f):
    "Show details of a callable object."
    print(" {}".format(name))
    print(" object:", f)
    print(" __name__:", end=" ")
    try:
        print(f.__name__)
    except AttributeError:
        print("no __name__()")
    print(" __doc__:", repr(f.__doc__))
    print()


def simple_decorator(f):
    @functools.wraps(f)
    def decorated(a="decorated defaults", b=1):
        print(" decorated:", (a, b))
        print(" ", end=" ")
        return f(a, b=b)
    return decorated


def myfunc(a, b=2):
    "myfunc() is not complicated"
    print(" myfunc:", (a, b))
    return


# The raw function
show_details("myfunc", myfunc)
myfunc("unwrapped, default b")
myfunc("unwrapped, passing b", 3)
print()

# Wrap explicitly
wrapped_myfunc = simple_decorator(myfunc)
show_details("wrapped_myfunc", wrapped_myfunc)
wrapped_myfunc()
wrapped_myfunc("args to wrapped", 4)
print()

# Wrap with decorator syntax
@simple_decorator
def decorated_myfunc(a, b):
    myfunc(a, b)
    return

show_details("decorated_myfunc", decorated_myfunc)
decorated_myfunc()
decorated_myfunc("args to decorated", 4)


""" Comparison """

import functools
import inspect
from pprint import pprint

""" Rich comparison """
# The rich comparison API is designed to allow classes with complex comparisons to implement each test in the most
# efficient way possible. However, for classes where comparison is relatively simple, there is no point in manually
# creating each of the rich comparison methods. The total_ordering() class decorator takes a class that provides some
# of the methods, and adds to them.

@functools.total_ordering
class MyObject:
    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        print(" testing __eq__({}, {})".format(
            self.val, other.val))
        return self.val == other.val

    def __gt__(self, other):
        print(" testing __gt__({}, {})".format(
            self.val, other.val
        ))
        return self.val > other.val


print("\nMethods:\n")
pprint(inspect.getmembers(MyObject, inspect.isfunction))

a = MyObject(10)
b = MyObject(5)

print("\nComparisons:")
for expr in ["a < b", "a <= b", "a == b", "a >= b", "a > b"]:
    print("\n{:<6}".format(expr))
    result = eval(expr)
    print("     result of {}: {}". format(expr, result))

print()

""" Caching """

# The lru_cache() decorator wraps a function in a least-recently-used cache. Arguments to the function are used to build
# a hash key, which is then mapped to the result. Subsequent calls with the same arguments will fetch the value from
# the cache instead calling the function. The decorator also adds methods to the function to examine the state of the
# cache (cache_info()) and empty the cache (cache_clear()).


@functools.lru_cache()
def expensive(a, b):
    print("expensive({}, {})".format(a, b))
    return a * b

MAX = 2

print("First set of calls:")
for i in range(MAX):
    for j in range(MAX):
        expensive(i, j)
print(expensive.cache_info())

print("\nSecond set of calls:")
for i in range(MAX + 1):
    for j in range(MAX + 1):
        expensive(i, j)
print(expensive.cache_info())

print("\nClearing cache:")
expensive.cache_clear()
print(expensive.cache_info())

print("\nThird set of calls:")
for i in range(MAX):
    for j in range(MAX):
        expensive(i, j)
print(expensive.cache_info())


# To prevent the cache from growing without bounds in a long-running process, it is given a maximum size. The default
# is 128 entries, but that can be changed for each cache using the maxsize argument.

@functools.lru_cache(maxsize=2)
def expensive_maxsize(a, b):
    print("called expensive({}, {})".format(a, b))
    return a * b


def make_call(a, b):
    print("({}, {})".format(a, b), end=" ")
    pre_hits = expensive_maxsize.cache_info().hits
    expensive(a, b)
    post_hits = expensive_maxsize.cache_info().hits

    if post_hits > pre_hits:
        print("cache hit")


print("Establish the cache")
make_call(1, 2)
make_call(2, 3)

print("\nUse cached items")
make_call(1, 2)
make_call(2, 3)

print("\nCompute a new value, triggering cache expiration")
make_call(3, 4)

print("\nCache still contains one old item")
make_call(2, 3)

print("\nOldest item needs to be recomputed")
make_call(1, 2)


# The keys for the cache managed by lru_cache() must be hashable, so all of the arguments to the function wrapped with
# the cache lookup must be hashable.


make_call(1, 2)

# If any object that can't be hashed is passed in to the function, a TypeError is raised.
try:
    make_call([1], 2)
except TypeError as err:
    print("ERROR: {}".format(err))

try:
    make_call(1, {"2": "two"})
except TypeError as err:
    print("ERROR: {}".format(err))

print()

""" Reducing a data set """

# The reduce() function takes a callable and a sequence of data as input and producesa a single value as output based on
# invoking the callable with the values from the sequence and accumulating the resulting output


# this example adds up the numbers in the input sequence
def do_reduce(a, b):
    print("do_reduce({}, {})".format(a, b))
    return a + b

data = range(1, 15)
print(data)

result  = functools.reduce(do_reduce, data)
print("result: {}".format(result))


# The optional initializer argument is placed at the front of the sequence and processed along with the other items.
# This can be used to update a previously computed value with new inputs.

# in this example a previous sum of 99 is used to initialize the value computed by reduce()
def do_reduce(a, b):
    print("do_reduce({}, {})".format(a, b))
    return a + b

data = range(1, 5)
print(data)
result = functools.reduce(do_reduce, data, 99)
print("result: {}".format(result))

# Sequences with a single item automatically reduce to that value when no initializer is present. Empty lists generate
# an error, unless an initializer is provided.


def do_reduce(a, b):
    print('do_reduce({}, {})'.format(a, b))
    return a + b


print('Single item in sequence:',
      functools.reduce(do_reduce, [1]))

print('Single item in sequence with initializer:',
      functools.reduce(do_reduce, [1], 99))

print('Empty sequence with initializer:',
      functools.reduce(do_reduce, [], 99))

try:
    print('Empty sequence:', functools.reduce(do_reduce, []))
except TypeError as err:
    print('ERROR: {}'.format(err))


""" Generic functions """

# In a dynamically typed language like Python it is common to need to perform slightly different operation based on
# the type of an argument, especially when dealing with the difference between a list of items and a single item.
# It is simple enough to check the type of an argument directly, but in cases where the behavioral difference can be
# isolated into separate functions functools provides the singledispatch() decorator to register a set of generic
# function for automatic switching based on the type of the first argument to a function.


# The function wrapped with singledispatch() is the default implementation if no other type-specific function is found,
# as with the float case in this example.
@functools.singledispatch
def myfunc(arg):
    print("default myfunc({!r})".format(arg))


# The register() attribute of the new function serves as another decorator for registering alternative implementations.
@myfunc.register(int)
def myfunc_int(arg):
    print("myfunc_int({})".format(arg))


@myfunc.register(list)
def myfunc_list(arg):
    print("myfunc_list()")
    for item in arg:
        print("      {}".format(item))


myfunc("string argument")
myfunc(1)
myfunc(2.3)
myfunc(["a", "b", "c"])


# When no exact match is found for the type, the inheritance order is evaluated and the closest matching type is used.

class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B):
    pass

class E(C, D):
    pass


@functools.singledispatch
def myfunc(arg):
    print("default myfunc({})".format(arg.__class__.__name__))


@myfunc.register(A)
def myfunc_A(arg):
    print("myfunc_A({})".format(arg.__class__.__name__))

@myfunc.register(B)
def myfunc_B(arg):
    print("myfunc_B({})".format(arg.__class__.__name__))

@myfunc.register(C)
def myfunc_C(arg):
    print("myfunc_C({})".format(arg.__class__.__name__))


myfunc(A())
myfunc(B())
myfunc(C())
myfunc(D())
myfunc(E())