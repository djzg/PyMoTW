#!/usr/bin/env/python3

""" ChainMap - Search multiple dictionaries """

# The ChainMap class manages a sequence of dictionaries, and searches through them in the order they are given to
# find values associated with keys. A ChainMap makes a good "context" container, since it can be treated as a stack for
# which changes happen as the stack grows, with these changes being discarded again as the stack shrinks.

""" Accessing values """

# The ChainMap supports the same API as a regular dictionary for accessing existing values

import collections

a = {"a": "A", "c": "C"}
b = {"b": "B", "c": "D"}

m = collections.ChainMap(a, b)

# The child mappings are searched in the order they are passeed to the constructor, so the value reported for the key
# "c" comes from the a dictionary.
print("Individual values")
print("a = {}".format(m["a"]))
print("b = {}".format(m["b"]))
print("c = {}".format(m["c"]))
print()

print("Keys = {}".format(list(m.keys())))
print("Values = {}".format(list(m.values())))
print()

print("Items:")
for k, v in m.items():
    print("{} = {}".format(k, v))
print()

print('"d" in m: {}'.format("d" in m))
print()


""" Reordering """
print("--- Reordering ---")

print(m.maps)
print("c = {}\n".format(m["c"]))

# reverse the list
m.maps = list(reversed(m.maps))
print(m.maps)
print("c = {}\n".format(m["c"]))    # when the list of mappings is reversed, the value associated with "c" changes
print()

""" Updating values """
print("--- Updating values ---")

# A ChainMap doesn't cache the values in the child mappings. Thus, if their contents are modified, the results are
# reflected when the ChainMap is accessed.
a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(a, b)
print("Before: {}".format(m["c"]))
a["c"] = "E"
print("After: {}".format(m["c"]))

# It is also possible to set values through the ChainMap directly, although only the first mapping in the chain
# is actually modified.
a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m = collections.ChainMap(a, b)
print("Before:", m)
m["c"] = "E"
print("After:", m)
print("a", a)

# ChainMap provides a convenience method for creating a new instance with one extra mapping at the front of the maps
# list to make it easy to avoid modifying the existing underlying data structures.

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}

m1 = collections.ChainMap(a, b)
m2 = m1.new_child()

print("m1 before:", m1)
print("m2 before:", m2)

m2["c"] = "E"

print("m1 after:", m1)
print("m2 after:", m2)

# This stacking behavior is what makes it convenient to use ChainMap instances as template or application contexts.
# Specifically, it is easy to add or update values in one iteration, then discard the changes for the next iteration.


# For situations where the new context is known or built in advance, it is also possible to pass a mapping to new_child()

a = {'a': 'A', 'c': 'C'}
b = {'b': 'B', 'c': 'D'}
c = {'c': 'E'}

m1 = collections.ChainMap(a, b)
m2 = m1.new_child(c)

print('m1["c"] = {}'.format(m1['c']))
print('m2["c"] = {}'.format(m2['c']))

# This is the equivalent of

m2 = collections.ChainMap(c, *m1.maps)

print(m2)

