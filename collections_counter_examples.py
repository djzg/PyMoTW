#!/usr/bin/env/python3

""" Counter - Count hashable objects """

# A Counter is a container that keeps track of how many times equivalent values are added. It can be used to implement
# the same algorithms for which other languages commonly use bag or multiset data structures.

""" Initializing """

# Counter supports three forms of initialization. Its constructor can be called with a sequence of items, a dictionary
# containing keys and counts, or using keyword arguments that map string names to counts.

import collections

print(collections.Counter(["a", "b", "c", "a", "b", "b"]))
print(collections.Counter({"a": 2, "b": 3, "c": 1}))
print(collections.Counter(a=2, b=3, c=1))

# An empty Counter can be constructed with no arguments and populated via the update() method.

c = collections.Counter()
print("Initial  :", c)

c.update("abcdaab")
print("Sequence :", c)

c.update({"a": 1, "d": 5})
print("Dict     :", c)


""" Accessing Counts """

# Once a Counter is populated, its values can be retrieved using the dictionary API.

c = collections.Counter("abcdaab")

for letter in "abcde":
    print("{} : {}".format(letter, c[letter]))

# Counter doesn't raise KeyError for unknown items. If a value has not been seen in the input, its count is 0.

# The elements() method returns an iterator that produces all of the items known to the Counter.

# The order of elements is not guaranteed, and items with counts less than or equal to zero are not included.
c["z"] = 0
print(c)
print(list(c.elements()))


# Use most_common() to produce a sequence of the n most frequently encountered input values and their respective counts.

c = collections.Counter()
with open("text.txt", "rt") as f:
    for line in f:
        c.update(line.rstrip().lower())
# This example counts the letters appearing in all of the words in the system dictionary to produce a frequency
# distribution, then prints the three most common letters. Leaving out the argument to most_common() produces a list
# of all items, in order of frequency.

print("Most common:")
for letter, count in c.most_common(3):
    print("{} : {}".format(letter, count))


""" Arithmetic """

# Counter instances support arithmetic and set operations for aggregating results. This example shows the standard
# operators for creating new Counter instance, but the in-place operators +=, -=, &=, and |= are also supported.

c1 = collections.Counter(['a', 'b', 'c', 'a', 'b', 'b'])
c2 = collections.Counter('antarctica')

print("C1:", c1)
print("C2:", c2)

print("\nCombined counts:")
print(c1 + c2)

print("\nSubstraction:")
print(c1 - c2)

print("\nIntersection (taking positive minimum:)")
print(c1 & c2)

print("\nUnion (taking maximums):")
print(c1 | c2)

# Each time a new Counter is produced through an operation, any items with zero or negative counts are discarded.




