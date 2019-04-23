#!/usr/bin/env/python3

""" defaultdict - Missing keys return a default value """

# The standard dictionary includes the method setdefault() for retrieving a value and establishing a default if the
# value does not exist. By contrast, defaultdict lets the caller specify the default up front when the container is
# initialized

import collections


def default_factory():
    return "default value"


d = collections.defaultdict(default_factory, foo="bar")

print("d:", d)
print("foo =>", d["foo"])
print("bar =>", d["bar"])

# This method works well as long as it is appropriate for all keys to have the same default. It can be especially
# useful if the default is a type used for aggregating or accumulating values, such as list, set or even int.
# The standard library documentation includes several examples in which defaultdict is used in this way.


