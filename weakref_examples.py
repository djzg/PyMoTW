#!/usr/bin/env/python3

""" weakref - Impermanent References to Objects """

# The weakref module supports weak references to objects. A normal reference increments the reference count on the
# object and prevents it from being garbage collected. This outcome is not always desirable, especially when a circular
# reference might be present or when a cache of objects should be deleted when memory is needed. A weak reference is a
# handle to an object that does not keep it from being cleaned up automatically.


""" References """

import weakref

class ExpensiveObject:

    def __del__(self):
        print("(Deleting {})".format(self))

obj = ExpensiveObject()
r = weakref.ref(obj)

print("obj:", obj)
print("ref:", r)
print("r():", r())

print("deleting obj")
del obj
print("r():", r())

# In this case, since obj is deleted before the second call to the reference, the ref returns None.

print("\n")
""" Reference callbacks """

# The ref constructor accepts an optional calback function that is invoked when the referenced object is deleted.

def callback(reference):
    """ Invoked when referenced object is deleted """
    print("callback({!r})".format(reference))

obj = ExpensiveObject()
r = weakref.ref(obj, callback)

print("obj:", obj)
print("ref:", r)
print("r():", r())

print("deleting obj")
del obj
print("r():", r())

# The callback receives the reference object as an argument after the reference is "dead" and no longer refers to the
# original object. One use for this feature is to remove the weak reference object from a cache.

print("\n")

""" Finalizing objects """

# For more robust management of resources when weak references are cleaned up, use finalize to associate callbacks
# with objects. A finalize instance is retained until the attached objects is deleted, even if the application does not
# retain a reference to the finalizer.

def on_finalize(*args):
    print("on_finalize({!r})".format(args))

obj = ExpensiveObject()
weakref.finalize(obj, on_finalize, "extra argument")
del obj

# The arguments to finalize are the object to track, a callable to invoke when the object is garbage collected, and any
# positional or named arguments to pass to the callable.

# The finalize instance has a writable property atexit to control whether the callback is invoked as a program is
# exiting, if it hasn't already been called.
print("\n")
import sys
import weakref

class ExpensiveObject:

    def __del__(self):
        print("Deleting {}".format(self))

def on_finalize(*args):
    print("on_finalize({!r})".format(args))

obj = ExpensiveObject()
f = weakref.finalize(obj, on_finalize, "Extra argument")
#f.atexit = bool(int(sys.argv[1]))


# Giving the finalize instance a reference to the object it tracks causes a reference to be retained, so the object
# is never garbage collected.

import gc
import weakref

class ExpensiveObject:

    def __del__(self):
        print('(Deleting {})'.format(self))


def on_finalize(*args):
    print('on_finalize({!r})'.format(args))


obj = ExpensiveObject()
obj_id = id(obj)

f = weakref.finalize(obj, on_finalize, obj)
f.atexit = False

del obj

for o in gc.get_objects():
    if id(o) == obj_id:
        print("found uncollected object in gc")

# As this example shows, even though the explicit reference to obj is deleted, the object is retained and visible to
# the garbage collector through f.


# Using a bound method of a tracked object as the callable can also prevent an object from being finalized properly.

import gc
import weakref


class ExpensiveObject:

    def __del__(self):
        print('(Deleting {})'.format(self))

    def do_finalize(self):
        print('do_finalize')


obj = ExpensiveObject()
obj_id = id(obj)

f = weakref.finalize(obj, obj.do_finalize)
f.atexit = False

del obj

for o in gc.get_objects():
    if id(o) == obj_id:
        print('found uncollected object in gc')

# Because the callable given to finalize is a bound method of the instance obj, the finalize object holds a reference
# to obj, which cannot be deleted and garbage collected.


""" Proxies """

# It is sometimes more convenient to use a proxy, rather than a weak reference. Proxies can be used as though they
# were the original object, and do not need to be called before the object is accessible. As a consequence, they can
# be passed to a library that does not know it is receiving a reference instead of the real object.

import weakref

class ExpensiveObject:

    def __init__(self, name):
        self.name = name

    def __del__(self):
        print("Deleting {}".format(self))

obj = ExpensiveObject("myobject")
r = weakref.ref(obj)
p = weakref.proxy(obj)

print("via obj:", obj.name)
print("via ref:", r().name)
print("via proxy:", p.name)
del obj
print("via proxy:", p.name)

# If the proxy is accesed after the referent object is removed, a ReferenceError exception is raised.


""" Caching objects """

# The ref and proxy classes are considered "low level". While they are useful for maintaining weak references to
# individual objects and allowing cycles to be garbage collected, the WeakKeyDictionary and WeakValueDictionary classes
# provide a more appropriate API for creating a cache of several objects.

import gc
from pprint import pprint
import weakref

gc.set_debug(gc.DEBUG_UNCOLLECTABLE)


class ExpensiveObject:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Expensive object({})".format(self.name)

    def __del__(self):
        print("     (Deleting {})".format(self))


def demo(cache_factory):
    # hold objects so any weak references are not removed immediately
    all_refs = {}
    # create the cache using the factory
    print("CACHE TYPE:", cache_factory)

    for name in ["one", "two", "three"]:
        o = ExpensiveObject(name)
        cache[name] = o
        all_refs[name] = o
        del o

    pprint("    all_refs = ", end=" ")
    pprint(all_refs)
    print("\n Before, cache contains:", list(cache.keys()))
    for name, value in cache.items():
        print("     {} = {}".format(name, value))
        del value

    # remove all references to the objects except the cache
    print("\nCleanup:")
    del all_refs
    gc.collect()

    print("\n After, cache contains:", list(cache.keys()))
    for name, value in cache.items():
        print("        {} = {}".format(name, value))
    print(" demo returning")
    return

demo(dict)
print()

demo(weakref.WeakValueDictionary)