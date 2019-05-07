#!/usr/bin/env/python3

""" heapq - Heap sort algorithm """

# A heap is a tree-like data structure in which the child nodes have a sort-order relationship with the parents.
# Binary heaps can be represented using a list or array organized so that the children of element N are at positions
# 2 * N + 1 and 2 * N + 2 (for zero-based indexes). This layout makes it possible to rearrange heaps in place, so
# it is not necessary to reallocate as much memory when adding or removing items.

# A max-heap ensures that the parent is larger than or equal to both of its children. A min-heap requires that the
# parent be less than or equal to its children. Python’s heapq module implements a min-heap.

""" Example data """
import math
import heapq
from io import StringIO

data = [19, 9, 4, 10, 11]

def show_tree(tree, total_width=36, fill=" "):
    # pretty-print a tree
    output = StringIO()
    last_row = -1
    for i, n in enumerate(tree):
        if i:
            row = int(math.floor(math.log(i + 1, 2)))
        else:
            row = 0
        if row != last_row:
            output.write("\n")
        columns = 2 ** row
        col_width = int(math.floor(total_width / columns))
        output.write(str(n).center(col_width, fill))
        last_row = row
    print(output.getvalue())
    print("-" * total_width)
    print()


""" Creating a heap """

# There are two basic ways to create a heap: heappush() and heapify()

heap = []
print("random :", data)
print()

# When heappush() is used, the heap sort order of the elements is maintained as new items are added from a data source.
for n in data:
    print("add {:>3}:".format(n))
    heapq.heappush(heap, n)
    show_tree(heap)


# If the data is already in memory, it is more efficient to use heapify() to rearrange the items of the list in place

print("random       :", data)
heapq.heapify(data)
print("heapified     :")
show_tree(data)

# The result of building a list in heap order one item at a time is the same as building an unordered list and then
# calling heapify()

""" Accessing the contents of a heap """

# Once the heap is organized correctly, use heappop() to remove the element with the lowest value

print("random       :", data)
heapq.heapify(data)
print("heapified    :")
show_tree(data)
print()

for i in range(2):
    smallest = heapq.heappop(data)
    print("pop      {:>3}:".format(smallest))
    show_tree(data)


# To remove existing elements and replace them with new values in a single operation, use heapreplace()
data = [19, 9, 4, 10, 11, 2, 27, 5, 49]
heapq.heapify(data)
print("start:")
show_tree(data)

for n in [0,13]:
    smallest = heapq.heapreplace(data, n)
    print("replace {:>2} with {:>2}".format(smallest, n))
    show_tree(data)


""" Data extremes from a heap """

# heapq also includes two functions to examine an iterable and find a range of the largest or smallest values it contains

print("all              :", data)
print("3 largest        :", heapq.nlargest(3, data))
print("from sort        :", list(reversed(sorted(data[-3:]))))
print("3 smallest       :", heapq.nsmallest(3, data))
print("from sort        :", sorted(data[:3]))

# Using nlargest() and nsmallest() is efficient only for relatively small values of n > 1, but can still come in handy
# in a few cases


""" Efficiently merging sorted sequences """

# Combining several sorted sequences into one new sequence is easy for small data sets
# list(sorted(itertools.chain(*data)))

# Instead of sorting the entire combined sequence, merge() uses a heap to generate a new sequence one item at a time,
# determining the next item using a fixed amount of memory

import random

random.seed(2019)

data = []

for i in range(4):
    new_data = list(random.sample(range(1, 101), 5))
    new_data.sort()
    data.append(new_data)

for i, d in enumerate(data):
    print("{} : {}".format(i, d))

print("\nMerged:")
for i in heapq.merge(*data):
    print(i, end=" ")
print()

# Because the implementation of merge() uses a heap, it consumes memory based on the number of sequences being merged
# rather than the number of items in those sequences.

