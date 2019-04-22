#!/usr/bin/env/python3

# The textwrap module can be used to format text for output in situations where pretty-printing is desired. It offers
# programmatic functionality similar to the paragraph wrapping or filling features found in many text editors and word
# processors.


""" Filling paragraphs """


import textwrap
from textwrap_example import sample_text

print(textwrap.fill(sample_text, width=50))

dedented_text = textwrap.dedent(sample_text)
print("Dedented:")
print(dedented_text)

# The dedented text can be passed through fill() with a few different width values

dedented_text = textwrap.dedent(sample_text).strip()
for width in [25, 60]:
    print("{} Columns: \n".format(width))
    print(textwrap.fill(dedented_text, width=width))
    print()

""" Indenting Blocks """
dedented_text = textwrap.dedent(sample_text)
wrapped = textwrap.fill(dedented_text, width=50)
wrapped += "\n\nSecond paragraph after a blank line."
final = textwrap.indent(wrapped, "> ")

print("Quoted block: \n")
print(final)

# To control which lines receive the new prefix, pass a callable as the predicate argument to indent().
# The callable will be invoked for each line of text in turn and the prefix will be added for lines where the return
# value is true.

def should_indent(line):
    print("Indent {!r}?".format(line))
    return len(line.strip()) % 2 == 0

dedented_text = textwrap.dedent(sample_text)
wrapped = textwrap.fill(dedented_text, width=50)
final = textwrap.indent(wrapped, "EVEN ",
                        predicate=should_indent)

print("\nQuoted block:\n")
print(final)

# This example adds the prefix EVEN to lines that contain an even number of characters


""" Hanging indents """
# In the same way that it is possible to set the width of the output, the indent of the first line can be controlled
# independently of subsequent lines.

dedented_text = textwrap.dedent(sample_text).strip()
print(textwrap.fill(dedented_text,
                    initial_indent="",
                    subsequent_indent="_" * 4,
                    width=50))


""" Truncating Long Text """

# Use shorten().

dedented_text = textwrap.dedent(sample_text)
original = textwrap.fill(dedented_text, width=50)

print("Original:\n")
print(original)

shortened = textwrap.shorten(original, 100, placeholder="[_ _ _]")
shortened_wrapped = textwrap.fill(shortened, width=50)

print("\nShortened:\n")
print(shortened_wrapped)

# The default placeholder value [...] can be replaced by providing a placeholder argument to shorten().

