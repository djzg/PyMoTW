#!/usr/bin/env/python3

""" itertools - Iterator functions """

# The functions provided by itertools are inspired by similar features of functional programming languages such as
# Clojure, Haskell, APL and SML. They are intended to be fast and use memory efficiently, and also to be hooked
# together to express more complicated iteration-based algorithms.

# Iterator-based code offers better memory consumption characteristics than code that uses lists. Since data is not
# produced from the iterator until it is needed all of the data does not need to be stored in memory at the same time.
# This "lazy" processing model can reduce swapping and other side-effects of large data sets, improving performance.

# In addition to the functions defined in itertools, the examples in this section also rely on some of the built-in
# functions for iteration.

""" Merging and splitting iterators """

# The chain() function takes several iterators as arguments and returns a single iterator that produces the contents
# of all of the inputs as though they came from a single iterator.

from itertools import *

for i in chain([1,2,3],["a","b","c"]):
    print(i, end=" ")

print()

# chain() makes it easy to process several sequences without constructing one large list.


# If the iterables to be combined are not all known in advance, or need to be evaluated lazily, chain.from_iterable()
# can be used to construct the chain instead.

def make_iterables_to_chain():
    yield [1, 2, 3]
    yield ["a", "b", "c"]

for i in chain.from_iterable(make_iterables_to_chain()):
    print(i, end=" ")
print()


# The built-in function zip() returns an iterator that combines the elements of several iterators into tuples.

for i in zip([1, 2, 3], ["a", "b", "c"]):
    print(i)

# As with the other functions in this module, the return value is an iterable object that produces values one at a time

# zip() stops when the first input iterator is exhausted. To process all the inputs, even if the iterators produce
# different numbers of values, use zip_longest()

r1 = range(3)
r2 = range(2)

print("\nzip stops early:")
print(list(zip(r1, r2)))

print("\nzip_longest processes all of the values:")
print(list(zip_longest(r1, r2)))
# By default, zip_longest() substitutes None for any missing values. Use the fillvalue argument to use a different
# substitute value.


# The islice() function returns an iterator which returns selected items from the input iterator, by index.

print("Stop at 5:")
for i in islice(range(100), 5):
    print(i, end=" ")
print("\n")

print("Start at 5, stop at 10:")
for i in islice(range(100), 5, 10):
    print(i, end=" ")
print("\n")

print("By tens to 100:")
for i in islice(range(100), 0, 100, 10):
    print(i, end=" ")
print("\n")
# islice() takes the same arguments as the slice operator for lists: start, stop and step. The start and step are optional.



# The tee() function returns several independent iterators (defaults to 2) based on a single original input.

r = islice(count(), 5)
i1, i2 = tee(r)

print("i1:", list(i1))
print("i2:", list(i2))

# The new iterators created by tee() share their input, so the original iterator should not be used after the new ones
# are created.

r = islice(count(), 5)
i1, i2 = tee(r)

print("r:", end=" ")
for i in r:
    print(i, end=" ")
    if i > 1:
        break
print()
# If values are consumed from the original input, the new iterators will not produce those values
print("i1:", list(i1))
print("i2:", list(i2))


""" Converting inputs """

# The built-in map() function returns an iterator that calls a function on the values in the input iterators, and
# returns the results. It stops when any input iterator is exhausted.

def times_two(x):
    return 2 * x

def multiply(x, y):
    return (x, y, x * y)

# In the first example, the lambda function multiplies the input values by 2. In a second example, the lambda function
# multiplies two arguments, taken from separate iterators, and returns a tuple with the original arguments and the
# computed value. The third example stops after producing two tuples because the second range is exhausted.
print("Doubles:")
for i in map(times_two, range(6)):
    print(i)

print("\nMultiples:")
r1 = range(6)
r2 = range(6, 10)
for i in map(multiply, r1, r2):
    print("{:d} * {:d} = {:d}".format(*i))

print("\nStopping:")
r1 = range(5)
r2 = range(5)
for i in map(multiply, r1, r2):
    print(i)
print()

# The starmap() is similar to map(), but instead of constructing a tuple from multiple iterators, it splits up the items
# in a single iterator as arguments to the mapping function using the * syntax.

values = [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]

for i in starmap(lambda x, y: (x, y, x * y), values):
    print("{} * {} = {}".format(*i))
# Where the mapping function to map() is called f(i1, i2), the mapping function passed to starmap() is called f(*i)
print()

""" Producing new values """

# The count() function returns an iterator that produces consecutive integers, indefinitely. The first number can be
# passed as an argument (the default is zero). There is no upper bound argument (see the built-in range() for more
# control over the result set).

for i in zip(count(1), ['a', 'b', 'c']):
    print(i)
# This example stops because the list argument is consumed
print()


# The start and step arguments to count() can be any numerical values that can be added together

import fractions

start = fractions.Fraction(1, 3)
step = fractions.Fraction(1, 3)


for i in zip(count(start, step), ["a", "b", "c"]):
    print("{}: {}".format(*i))
# In this example, the start point and steps are Fraction objects from the fraction module
print()



# The cycle() function returns an iterator that repeats the contents of the arguments it is given indefinitely.
# Since it has to remember the entire contents of the input iterator, it may consume quite a bit of memory if the
# iterator is long

for i in zip(range(7), cycle(['a', 'b', 'c'])):
    print(i)
# A counter variable is used to break out of the loop after a few cycles in this example.
print()



# The repeat() function returns an iterator that produces the same value each time it is accessed.

for i in repeat("over-and-over", 5):
    print(i)


# It is useful to combine repeat() with zip() or map() when invariant values need to be included with the values from
# the other iterators.

for i, s in zip(count(), repeat("over-and-over", 5)):
    print(i, s)
print()

# This example uses map() to multiply the numbers in the range 0 through 10 by 2
for i in map(lambda x, y: (x, y, x * y), repeat(2), range(10)):
    print("{:d} * {:d} = {:d}".format(*i))
# The repeat() iterator does not need to be explicitly limited, since map() stops processing when any of its inputs ends,
# and the range() returns only five elements.


""" Filtering """

# The dropwhile() function returns an iterator that produces elements of the input iterator after a condition becomes
# false for the first time.

def should_drop(x):
    print("Testing:", x)
    return x < 1

for i in dropwhile(should_drop, [-1, 0, 1, 2, -2]):
    print("Yielding:" , i)
# dropwhile() does not filter every item of the input; after the condition is false the first time, all of the remaining
# items in the input are returned
print()

# The opposite of dropwhile() is takewhile(). It returns an iterator that returns items from the input iterator as long
# as the test function returns true.

def should_take(x):
    print("Testing:", x)
    return x < 2

for i in takewhile(should_take, [-1, 0, 1, 2, -3]):
    print("Yielding:" , i)
# As soon as should_take() returns False, takewhile() stops processing the input.
print()

# The built-in function filter() returns an iterator that includes only items for which the test function returns true.

def check_item(x):
    print("Testing:", x)
    return x < 1

for i in filter(check_item, [-1, 0, 1, 2, -2]):
    print("Yielding", i)
# filter() is different from dropwhile() and takewhile() in that every item is tested before it is returned.
print()


# filterfalse() returns an iterator that inlcudes only items where the test function returns false.

def check_item(x):
    print('Testing:', x)
    return x < 1


for i in filterfalse(check_item, [-1, 0, 1, 2, -2]):
    print('Yielding:', i)


# compress() offers another way to filter the contents of an iterable. Instead of calling a function, it uses the
# values in another iterable to indicate when to accept a value and when to ignore it.

every_third = cycle([False, False, True])
data = range(1, 100)

for i in compress(data, every_third):
    print(i, end=" ")
print()


""" Grouping data """

# The groupby() function returns an iterator that produces sets of values organized by a common key. This example
# illustrates grouping related values based on an attribute.

import functools
from itertools import *
import operator
import pprint

@functools.total_ordering
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __gt__(self, other):
        return (self.x, self.y) > (other.x, other.y)

# Create a dataset of Point instances
data = list(map(Point,
                cycle(islice(count(), 3)),
                islice(count(), 7)))

print("Data:")
pprint.pprint(data, width=35)
print()

# Try to group the unsorted data based on X values
print("Grouped, unsorted:")
for k, g in groupby(data, operator.attrgetter("x")):
    print(k, list(g))
print()

# Sort the data
data.sort()
print("Sorted:")
pprint.pprint(data, width=35)
print()

# Group the sorted data based on X values
print("Grouped, sorted:")
for k, g in groupby(data, operator.attrgetter("x")):
    print(k, list(g))
# The input sequence needs to be sorted on the key value in order for the groupings to work out as expected.
print()


""" Combining inputs """

# The accumulate() function processes the input iterable, passing the nth and n+1st item to a function and producing
# the return value instead of either input. The default function used to combine the two values adds them, so
# accumulate() can be used to produce the cumulative sum of a series of numerical inputs.

print(list(accumulate(range(10))))
print(list(accumulate("abcde")))
# When used with a sequence of non-integer values, the results depend on what it means to "add" two items together.
# The second example shows that when accumulate() receives a string input each response is a progressively longer
# prefix of that string.


# It is possible to combine accumulate() with any other function that takes two input values to achieve different results.

def f(a, b):
    print(a, b)
    return b + a + b

print(list(accumulate("abcde", f)))
# This example combines the string values in a way that makes a series of (nonsensical) palindromes. Each step of the
# way when f() is called, it prints the input values passed to it by accumulate()
print()


# Nested for loops that iterate over multiple sequences can often be replaced with product(), which produces a single
# iterable whose values are the Cartesian product of the set of input values


FACE_CARDS = ("J", "Q", "K", "A")
SUITS = ("H", "C", "D", "S")

DECK = list(
    product(
        chain(range(2, 11), FACE_CARDS),
        SUITS,
    )
)

for card in DECK:
    print("{:>2}{}".format(*card), end=" ")
    if card[1] == SUITS[-1]:
        print()
print()
# The values produced by product() are tuples, with the members taken from each of the iterables passed in as arguments
# in the order they are passed. The first tuple returned includes the first value from each iterable. The last iterable
# passed to product() is processed first, followed by the next to last, and so on. The result is that the return values
# are in order based on the first iterable, then the next iterable, etc.
# In this example, cards are ordered by value then by suit.
# To change the order of the cards, change the order of the arguments to product()

DECK = list(
    product(
        SUITS,
        chain(range(2,11), FACE_CARDS),
    )
)

for card in DECK:
    print("{:>2}{}".format(card[1], card[0], end=" "))
    if card[1] == FACE_CARDS[-1]:
        print()
# The print loop in this example looks for an Ace card, instead of the spade suit, and then adds a newline to break up
# the output.


# To compute the product of a sequence with itself, specify how many times the input should be repeated.


def show(iterable):
    for i, item in enumerate(iterable, 1):
        print(item, end=" ")
        if (i % 3) == 0:
            print()
    print()

print("Repeat 2:\n")
show(list(product(range(5), repeat=2)))
print("\n")
print("Repeat 3:\n")
show(list(product(range(5), repeat=2)))


# The permutations() function produces items from the input iterable combined in the possible permutations of the given
# length. It defaults to producing the full set of all permutations.

def show(iterable):
    first = None
    for i, item in enumerate(iterable, 1):
        if first != item[0]:
            if first is not None:
                print()
            first = item[0]
        print("".join(item), end=" ")
    print()

print("All permutations:\n")
show(permutations("abcde"))
print("\nPairs:\n")
# Use the r argument to limit the length and number of the individual permutations returned
show(permutations("abcd", r=3))
print()

# To limit the values to unique combinations rather than permutations, use combinations(). As long as the members of
# the input are unique, the output will not include any repeated values.

def show(iterable):
    first = None
    for i, item in enumerate(iterable, 1):
        if first != item[0]:
            if first is not None:
                print()
            first = item[0]
        print("".join(item), end=" ")
    print()

print("Unique pairs:\n")
show(combinations("abcdef", r=4))
print()

# While combinations() does not repeat individual input elements, sometimes it is useful to consider combinations that
# do include repeated elements. For those cases, use combinations_with_replacement()

def show(iterable):
    first = None
    for i, item in enumerate(iterable, 1):
        if first != item[0]:
            if first is not None:
                print()
            first = item[0]
        print("".join(item), end=" ")
    print()

print("Unique pairs:\n")
show(combinations_with_replacement("abcd", r=2))
# In this output, each input item is paired with itself as well as all of the other members of the input sequence

