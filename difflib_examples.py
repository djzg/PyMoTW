#!/usr/bin/env/python3

# The difflib module contains tools for computing and working with differences between sequencess.
# It is especially useful for comparing text, and includes functions that produce reports using several common
# difference formats.

import difflib

text1 = """Lorem ipsum dolor sit amet, consectetuer adipiscing
elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
pulvinar porttitor tellus. Aliquam venenatis. Donec facilisis
pharetra tortor.  In nec mauris eget magna consequat
convalis. Nam sed sem vitae odio pellentesque interdum. Sed
consequat viverra nisl. Suspendisse arcu metus, blandit quis,
rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Suspendisse eu lectus. In nunc. Duis vulputate
tristique enim. Donec quis lectus a justo imperdiet tempus."""

text1_lines = text1.splitlines()

text2 = """Lorem ipsum dolor sit amet, consectetuer adipiscing
elit. Integer eu lacus accumsan arcu fermentum euismod. Donec
pulvinar, porttitor tellus. Aliquam venenatis. Donec facilisis
pharetra tortor. In nec mauris eget magna consequat
convalis. Nam cras vitae mi vitae odio pellentesque interdum. Sed
consequat viverra nisl. Suspendisse arcu metus, blandit quis,
rhoncus ac, pharetra eget, velit. Mauris urna. Morbi nonummy
molestie orci. Praesent nisi elit, fringilla ac, suscipit non,
tristique vel, mauris. Curabitur vel lorem id nisl porta
adipiscing. Duis vulputate tristique enim. Donec quis lectus a
justo imperdiet tempus.  Suspendisse eu lectus. In nunc."""

text2_lines = text2.splitlines()


""" Comparing bodies of text """

# Lines prefixed with - were in the first sequence, but not the second
# Lines prefixed with + were in the second sequence but not the first.
# If a line has an incremental difference between versions, an extra line prefixed with ? is used to highlight the change
# If a line has not changed, it is printed with an extra blank space on the left column so that it is aligned with the
# other output that may have differences

d = difflib.Differ()
diff = d.compare(text1_lines, text2_lines)
print("\n".join(diff))

""" Other output formats """

# unified_diff() function includes only the modified lines and a bit of context

diff = difflib.unified_diff(
    text1_lines,
    text2_lines,
    lineterm="",        # lineterm argument is used to tell unified_diff() to skip appending newlines to the control lines
                        # that it returns because the input lines do not include them.
    )
print("\n".join(diff))

""" Junk data """

# All of the functions that produce difference sequences accept arguments to indicate which lines should be ignored and
# which characters within a line should be ignored. These parameters can be used to skip over markup or whitespace
# changes in two versions of a file, for example.

from difflib import SequenceMatcher


def show_results(match):
    print("  a   = {}".format(match.a))
    print("  b   = {}".format(match.b))
    print(" size = {}".format(match.size))
    i, j, k = match
    print("  A[a:a+size] = {!r}".format(A[i:i + k]))
    print("  B[b:b+size] = {!r}".format(B[j:j + k]))


A = " abcd"
B = "abcd abcd"

print("A = {!r}".format(A))
print("B = {!r}".format(B))

print("\nWithout junk detection:")
s1 = SequenceMatcher(None, A, B)
match1 = s1.find_longest_match(0, len(A), 0, len(B))
show_results(match1)

print("\nTreat spaces as junk:")
s2 = SequenceMatcher(lambda x: x == " ", A, B)
match2 = s2.find_longest_match(0, len(A), 0, len(B))
show_results(match2)


""" Comparing arbitrary types """

# The SequenceMatcher class compares two sequences of any types, as long as the values are hashable. It uses an
# algorithm to identify the longest contiguous matching blocks from the sequences, eliminating “junk” values that
# do not contribute to the real data.
#
# The funct get_opcodes() returns a list of instructions for modifying the first sequence to make it match the second.
# The instructions are encoded as five-element tuples, including a string instruction (the “opcode”, see the table
# below) and two pairs of start and stop indexes into the sequences (denoted as i1, i2, j1, and j2).

# difflib.get_opcodes() instructions
# "replace"   Replace a[i1:i2] with b[j1:j2]
# "delete"    Remove a [i1:i2] entirely
# "insert"    Insert b[j1:j2] at a[i1:i1]
# "equal"     The subsequences are already equal

s1 = [1, 2, 3, 4, 5, 6]
s2 = [2, 3, 5, 4, 6, 1]

print("Initial data:")
print("s1=", s1)
print("s2=", s2)
print("s1==s2:", s1 == s2)
print()

# This example compares two lists of integers and uses get_opcodes() to derive the instructions for converting the
# original list into the newer version. The modifications are applied in reverse order so that the list indexes
# remain accurate after items are added and removed.
matcher = difflib.SequenceMatcher(None, s1, s2)
for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):

    if tag == "delete":
        print("Remove {} from positions [{}:{}]".format(
            s1[i1:i2], i1,i2))
        print("  befpre =", s1)
        del s1[i1:i2]

    elif tag == "equal":
        print("s1[{}:{}] and s2[{}:{}] are the same".format(
            i1, i2, j1, j2))

    elif tag == "insert":
        print("Insert {} from s2[{}:{}] into s1 at {}".format(
            s2[j1:j2], j1, j2, i1))
        print("  before =", s1)
        s1[i1:i2] = s2[j1:j2]

    elif tag == "replace":
        print("Replace {} from s1[{}:{}] with {} from s2[{}:{}]".format(
            s1[i1:i2], i1, i2, s2[j1:j2], j1, j2))
        print("  before =", s1)
        s1[i1:i2] = s2[j1:j2]

    print("  after =", s1, "\n")

print("s1 == s2:", s1 == s2)

# SequenceMatcher works with custom classes, as well as built-in types, as long as they are hashable.

