#!/usr/bin/env/python3

""" array - Sequence of fixed-type data """

# The array module defines a sequence of data structure that looks very much like a list, except that all of the
# members have to be of the same primitive type. The types supported are all numeric or other fixed-size primitive
# types such as bytes.

# Refer to the table below for some of the supported types.
# Code 	Type 	Minimum size (bytes)
# b 	int 	1
# B 	int 	1
# h 	signed short 	2
# H 	unsigned short 	2
# i 	signed int 	2
# I 	unsigned int 	2
# l 	signed long 	4
# L 	unsigned long 	4
# q 	signed long long 	8
# Q 	unsigned long long 	8
# f 	float 	4
# d 	double float 	8

""" Initialization """

# An array is instantiated with an argument describing the type of data to be allowed, and possibly an initial sequence
# of data to store in the array.

import array
import binascii

# In this example, the array is configured to hold a sequence of bytes and is initialized with a simple byte string.
s = b'This is the array.'
a = array.array("b", s)

print("As byte string   :", s)
print("As array         :", a)
print("As hex           :", binascii.hexlify(a))

""" Manipulating arrays """

# An array can be extended and otherwise manipulated in the same ways as other Python sequences.

import pprint

a = array.array("i", range(3))
print("Initial  :", a)

# The supported operations include slicing, iterating and adding elements to the end

a.extend(range(3))
print("Extended :", a)

print("Slice    :", a[2:5])

print("Iterator:")
print(list(enumerate(a)))

""" Arrays and files """

# The contents of an array can be written to and read from files using built-in methods coded efficiently for that
# purpose.

import tempfile

a = array.array("i", range(6))
print("A1:", a)

# Write the array of numbers to a temporary file
output = tempfile.NamedTemporaryFile()
a.tofile(output.file)   # must pass an actual file
output.flush()

# read the raw data
# with open(output.name, "r") as input:
#     raw_data = input.read()
#     print("Raw contents:", binascii.hexlify(raw_data))
#
#     # Read the data into an array
#     input.seek(0)
#     a2 = array.array("i")
#     a2.fromfile(input, len(a))
#     print("A2:", a2)

""" Alternative byte ordering """

# If the data in the array is not in the native byte order, or if the data needs to be swapped before being sent to a
# system with a different byte order (or over the network), it is possible to convert the entire array without iterating
# over the elements from Python.

def to_hex(a):
    chars_per_item = a.itemsize * 2  # 2 hex digits
    hex_version = binascii.hexlify(a)
    num_chunks = len(hex_version) // chars_per_item
    for i in range(num_chunks):
        start = i * chars_per_item
        end = start + chars_per_item
        yield hex_version[start:end]


start = int('0x12345678', 16)
end = start + 5
a1 = array.array('i', range(start, end))
a2 = array.array('i', range(start, end))

# The byteswap() method switches the byte order of the items in the array from within C, so it is much more efficient
# than looping over the data in Python.
a2.byteswap()

fmt = '{:>12} {:>12} {:>12} {:>12}'
print(fmt.format('A1 hex', 'A1', 'A2 hex', 'A2'))
print(fmt.format('-' * 12, '-' * 12, '-' * 12, '-' * 12))
fmt = '{!r:>12} {:12} {!r:>12} {:12}'
for values in zip(to_hex(a1), a1, to_hex(a2), a2):
    print(fmt.format(*values))
