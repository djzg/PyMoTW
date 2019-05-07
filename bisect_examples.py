#!/usr/bin/env/python3

""" bisect - Maintain lists in sorted order """

# The bisect module implements an algorithm for inserting elements into a list while maintaining the list in sorted order.

""" Inserting in sorted order """

import bisect

# a series of random numbers
values = [14, 85, 77, 26, 50, 45, 66, 79, 10, 3, 84, 77, 1]

print("New Pos Contents")
print("--- --- --------")

l = []
for i in values:
    position = bisect.bisect(l, i)
    bisect.insort(l, i)
    print("{:3}{:3}".format(i, position), l)

# The first column of the output shows the new random number. The second column shows the position where the number
# will be inserted into the list. The remainder of each line is the current sorted list.

#  For long lists, significant time and memory savings can be achieved using an insertion sort algorithm such as this,
#  especially when the operation to compare two members of the list requires expensive computation.


""" Handling duplicates """

values = [14, 85, 77, 26, 50, 45, 66, 79, 10, 3, 84, 77, 1]

print('New  Pos  Contents')
print('---  ---  --------')

# Use bisect_left and insort_left.
l = []
for i in values:
    position = bisect.bisect_left(l, i)
    bisect.insort_left(l, i)
    print('{:3}  {:3}'.format(i, position), l)

# When the same data is manipulated using bisect_left() and insort_left(), the results are the same sorted list but the
# insert positions are different for the duplicate values.
