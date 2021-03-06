#!/usr/bin/env/python3


""" struct - Binary data structures """

# The struct module includes functions for converting between strings of bytes and native Python data types such as
# numbers and strings


""" Packing and unpacking """

# Struct supports packing data into strings, and unpacking data from strings using format specifiers made up of characters
# representing the type of the data and optional count and endianness indicators.

# In this example, the specifier calls for an integer or long integer value, a two-byte string, and a floating-point
# number. The spaces in the format specifier are included to separate the type indicators, and are ignored when the
# format is compiled

import struct
import binascii

values = (1, "ab".encode("utf-8"), 2.7)
s = struct.Struct("I 2s f")
packed_data = s.pack(*values)

print("Original values  :", values)
print("Format string    :", s.format)
print("Uses             :", s.size, "bytes")
# The example converts the packed value to a sequence of hex bytes for printing with binascii.hexlify() since some
# of the characters are nulls.
print("Packed value     :", binascii.hexlify(packed_data))

packed_data = binascii.unhexlify(b'0100000061620000cdcc2c40')

s = struct.Struct("I 2s f")
unpacked_data = s.unpack(packed_data)
print("Unpacked values:", unpacked_data)
print()


""" Endianness """

# By default, values are ncoded using the native C library notion of endianness. It is easy to override that choice
# by providing an explicit endianness directive in the format string.

value = (1, "ab".encode("utf-8"), 3.7)
print("Original values:", values)


endianness = [
    ("@", "native, native"),
    ("=", "native, standard"),
    ("<", "little-endian"),
    (">", "big-endian"),
    ("!", "network"),
]

for code, name in endianness:
    s = struct.Struct(code + "I 2s f")
    packed_data = s.pack(*values)
    print()
    print("Format string    :", s.format, "for", name)
    print("Uses             :", s.size, "bytes")
    print("Packed value     :", binascii.hexlify(packed_data))
    print("Unpacked value   :", s.unpack(packed_data))

print()

""" Buffers """

# Working with binary packed data is typically reserved for performance-sensitive situations or passing data into and
# out of extension modules. These cases can be optimized by avoiding the overhead of allocating a new buffer for each
# packed structure. The pack_into() and unpack_from() methods support writing to pre-allocated buffers directly.

import array
import binascii
import ctypes
import struct

s = struct.Struct("I 2s f")
values = (1, "ab".encode("utf-8"), 5.34)
print("Original:", values)
print()

print("ctypes string buffer")

b = ctypes.create_string_buffer(s.size)
print("Before   :", binascii.hexlify(b.raw))
s.pack_into(b, 0, *values)
print("After    :", binascii.hexlify(b.raw))
print("Unpacked :", s.unpack_from(b, 0))

print()
print("array")

a = array.array("b", b"\0" * s.size)
print("Before   :", binascii.hexlify(a))
s.pack_into(a, 0, *values)
print("After    :", binascii.hexlify(a))
print("Unpacked :", s.unpack_from(a, 0))

