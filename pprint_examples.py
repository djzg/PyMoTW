#!/usr/bin/env/python3


""" pprint - Pretty-print Data structures """

# The pprint module contains a "pretty printer" for producing aesthetically pleasing views of data structures.
# The formatter produces representations of data structures that can be parsed correctly by the interpreter, and that
# are also easy for a human to read. The output is kept on a single line, if possible, and indented when split across
# multiple lines.


data = [
    (1, {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}),
    (2, {'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H',
         'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L'}),
    (3, ['m', 'n']),
    (4, ['o', 'p', 'q']),
    (5, ['r', 's', 't''u', 'v', 'x', 'y', 'z']),
]


""" Printing """
from pprint import pprint

print("PRINT:")
print(data)
print()
print("PPRINT:")
# pprint() formats an object and writes it to the data stream passed in as an argument (or sys.stdout by default).
pprint(data)

""" Formatting """

# To format a data structure without writing it directly to a stream, use pformat() to build a string representation.

import logging
from pprint import pformat

logging.basicConfig(
    level=logging.DEBUG,
    format=" %(levelname) -8s %(message)s",
)

logging.debug("Logging pformatted data")
formatted = pformat(data)
for line in formatted.splitlines():
    logging.debug(line.rstrip())


""" Arbitrary classes """

# The PrettyPrinter class used by pprint() can also work with custom classes, if they define a __repr__() method

class node:
    def __init__(self, name, contents=[]):
        self.name = name
        self.contents = contents[:]

    def __repr__(self):
        return (
            "node(" + repr(self.name) + ", " +
            repr(self.contents) + ")"
        )

trees = [
    node("node-1"),
    node("node-2", [node("node-2-1")]),
    node("node-3", [node("node-3-1")]),
]

pprint(trees)


""" Recursion """

# Recursive data structures are represented with a reference to the original source of the data, given in the format
# <Recursion on typename with id=number>

local_data = ["a", "b", 1, 23]
# In this example, the list local_data is added to itself, creating a recursive reference
local_data.append(local_data)

print("id(local_data) =>", id(local_data))
pprint(local_data)


""" Limiting nested output """

pprint(data, depth=1)
pprint(data, depth=2)

""" Controlling output width"""

# The default output width for the formatted text is 80 columns. To adjust that width, use width argument to pprint()

for width in [80, 15]:
    print("WIDTH =", width)
    pprint(data, width=width)
    print()

# The compact flag tells pprint() to try to fit more data on each individual line, rather than spreading complex data
# structures across lines

print("DEFAULT:")
pprint(data, compact=False)
print("\nCOMPACT:")
pprint(data, compact=True)
