#!/usr/bin/env/python3

""" namedtuple - Tuple Subclass with named fields"""


# The standard tuple uses numerical indexes to access its members.
# This makes tuples convenient for simple uses

bob = ("Bob", 30, "male")
print("Representation:", bob)

jane = ("Jane", 29, "female")
print("\nField by index:", jane[0])

print("\nFields by index:")
for p in [bob, jane]:
    print("{} is a {} year old {}".format(*p))

# In contrast, remembering which index should be used for each value can lead to errors, especially if the tuple has a
# lot of fields and is constructed far from where it is used. A named tuple, assigns names, as well as the numerical
# index, to each number.

""" Defining """

# namedtuple instances are just as memory efficient as regular tuples because they do not have per-instance dictionaries.
# Each kind of namedtuple is represented by its own class, which is created by using the namedtuple() function.
# The arguments are the name of the new class and a string containing the names of the elements.

import collections

Person = collections.namedtuple("Person", "name age")

bob = Person(name="Bob", age=30)
print("\nRepresentation:", bob)

jane = Person(name="Jane", age=29)
print("\nField by name:", jane.name)

print("\nFields by index:")
for p in [bob, jane]:
    print("{} is {} years old.".format(*p))

# Just like a regular tuple, a namedtuple is immutable. This restriction allows tuple instances to have a consistent
# hash value, which makes it possible to use them as keys in dictionaries and to be included in sets.
# Trying to change a value through its named attribute results in an AttributeError

#bob.age = 25

""" Invalid field names """

# Field names are invalid if they are repeated or conflict with Python keywords.
try:
    collections.namedtuple("Person", "name class age")
except ValueError as err:
    print(err)

try:
    collections.namedtuple("Person", "name age age")
except ValueError as err:
    print(err)

""" Special attributes """

# namedtuple provides several useful attributes and methods for working with subclasses and instances. All of these
# built-in properties have names prefixed with an underscore(_), which by convention in most Python programs indicates
# a private attribute. For namedtuple, however, the prefix is intended to protect the name from collision with
# user-provided attribute names.

print("Fields:", bob._fields)

# namedtuple instances can be converted to OrderedDict instances using _asdict()

print(bob._asdict())

# The _replace() method builds a new instance, replacing the values of some fields in the process.

print("\nBefore:", bob)

# Although the name implies it is modifying the existing object, because namedtuple instances are immutable the method
# actually returns a new object.
bob2 = bob._replace(name="Robert")
print("After:", bob2)
print("Same?:", bob is bob2)


