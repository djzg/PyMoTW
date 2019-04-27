#!/usr/bin/env/python3

""" OrderedDict - Remember the order keys are added to a dictionary """

# An OrderedDict is a dictionary subclass that remembers the order in which its contents are added

from collections import OrderedDict

print("Regular Dictionary:")
d = {}

d["a"] = "A"
d["b"] = "B"
d["c"] = "C"

for k,v in d.items():
    print(k,v)

print("\nOrderedDict:")
d = OrderedDict()
d["a"] = "A"
d["b"] = "B"
d["c"] = "C"

for k,v in d.items():
    print(k,v)

""" Equality """

print("dict         :", end=" ")
d1 = {}
d1["a"] = "A"
d1["b"] = "B"
d1["c"] = "C"

d2 = {}
d2["a"] = "A"
d2["b"] = "B"
d2["c"] = "C"

print(d1 == d2)

print("OrderedDict  :", end=" ")
d1 = OrderedDict()
d1["a"] = "A"
d1["b"] = "B"
d1["c"] = "C"

# In this case, since the two ordered dictionaries are created from values in a different order, they are considered
# to be different.

d2 = OrderedDict()
d2["c"] = "C"
d2["b"] = "B"
d2["a"] = "A"
print(d1 == d2)


""" Reordering """

# It is possible to change the order of the keys in an OrderedDict by moving them to either the beginning or the end
# of the sequence using move_to_end()

d = OrderedDict(
    [('a', 'A'), ('b', 'B'), ('c', 'C')]
)

print('Before:')
for k, v in d.items():
    print(k, v)

d.move_to_end('b')

print('\nmove_to_end():')
for k, v in d.items():
    print(k, v)

# The last argument tells move_to_end() whether to move the item to be the last item in the key sequence or the first
d.move_to_end('b', last=False)

print('\nmove_to_end(last=False):')
for k, v in d.items():
    print(k, v)