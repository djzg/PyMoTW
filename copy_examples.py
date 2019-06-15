#!/usr/bin/env/python3

""" copy - Duplicate objects """

# Provides functions for duplicating objects using shallow or deep copy semantics

# The copy module includes two functions, copy() and deepcopy(), for duplicating existing objects.


""" Shallow copies """

# The shallow copy created by copy() is a new container populated with references to the contents of the original object.
# When making a shallow copy of a list object, a new list is constructed and the elements of the original object
# are appended to it.

import copy
import functools

@functools.total_ordering
class MyClass:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.name > other.name

a = MyClass("a")
my_list = [a]
dup = copy.copy(my_list)

print("             my list:", my_list)
print("                 dup:",  dup)
print("      dup is my_list:", (dup is my_list))
print("      dup == my_list:", (dup == my_list))
print("dup[0] is my_list[0]:", (dup[0] is my_list[0]))
print("dup[0] == my_list[0]:", (dup[0] == my_list[0]))
print("\n")

""" Deep copies """

# The deep copy created by deepcopy() is a new container populated with copies of the contents of the original object.
# To make a deep copy of a list, a new list is constructed, the elements of the original list are copied, and then
# those copies are appended to the new list.


@functools.total_ordering
class MyClass:

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.name > other.name


a = MyClass('a')
my_list = [a]
dup = copy.deepcopy(my_list)

print('             my_list:', my_list)
print('                 dup:', dup)
print('      dup is my_list:', (dup is my_list))
print('      dup == my_list:', (dup == my_list))
print('dup[0] is my_list[0]:', (dup[0] is my_list[0]))
print('dup[0] == my_list[0]:', (dup[0] == my_list[0]))
print()
# The first element of the list is no longer the same object reference, but when the two objects are compared they
# still evaluate as being equal



""" Customizing copy behavior """

# It is possible to control how copies are made using the __copy__() and __deepcopy__() special methods.

# __copy__() is called without any arguments and should return a shallow copy of the object
# __deepcopy__() is called with a memo dictionary and should return a deep copy of the object. Any member attributes
# that need to be deep-copied should be passed to copy.deepcopy(), along with the memo dictionary, to control for
# recursion.

import copy
import functools

@functools.total_ordering
class MyClass:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return self.name > other.name

    def __copy__(self):
        print("__copy__()")
        return MyClass(self.name)

    def __deepcopy__(self, memo):
        print("__deepcopy__()".format(memo))
        return MyClass(copy.deepcopy(self.name, memo))


a = MyClass("a")

sc = copy.copy(a)
dc = copy.deepcopy(a)


""" Recursion in Deep Copy """

# To avoid problems with duplicating recursive data structures, deepcopy() uses a dictionary to track objects that have
# already been copied. This dictionary is passed to the __deepcopy__() method so it can be examined there as well.

# The next example shows how an interconnected data structure such as a directed graph can help protect against
# recursion by implementing a __deepcopy__() method.

import copy

class Graph:

    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

    # The add_connection() method is used to set up bidirectional connections. It is also used by the deep copy operator.
    def add_connection(self, other):
        self.connections.append(other)

    def __repr__(self):
        return "Graph(name={}, id={})".format(
            self.name, id(self)
        )
    # The __deepcopy__() method prints messages to show how it is called, and manages the memo dictionary contents as
    # needed. Instead of copying the entire connection list wholesale, ti creates a new list and appends copies of the
    # individual connections to it. That ensures that the memo dictionary is updated as each new node is duplicated,
    # and avoids recursion issues of extra copies of nodes. As before, the method returns the copied object when it is
    # done.
    def __deepcopy__(self, memo):
        print("\nCalling __deepcopy__ for {!r}".format(self))
        if self in memo:
            existing = memo.get(self)
            print("     Already copied to {!r}".format(existing))
            return existing
        print("Memo dictionary:")
        if memo:
            for k, v in memo.items():
                print("     {}: {}".format(k, v))
        else:
            print("     (empty)")

        dup = Graph(copy.deepcopy(self.name, memo), [])
        print("     Copying to new object {}".format(dup))
        memo[self] = dup
        for c in self.connections:
            dup.add_connection(copy.deepcopy(c, memo))
        return dup

root = Graph("root", [])
a = Graph("a", [root])
b = Graph("b", [a, root])
root.add_connection(a)
root.add_connection(b)

dup = copy.deepcopy(root)
