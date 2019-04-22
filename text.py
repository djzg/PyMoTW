#!/usr/bin/env/python3

# The string module dates from the earliest versions of Python. Many of the functions previously implemented in this
# module have been moved to methods of str objects. The string module retains several useful constants and classes for
# working with str objects. This discussion will concentrate on them.

import string

# Function capwords() capitalizes all of the words in a string

s = 'The quick brown fox jumped over the lazy dog.'

print(s)
print(string.capwords(s))

# String templates were added as part of PEP 292 and are intended as an alternative to the built-in interpolation syntax.
# With string.Template interpolation, variables are identified by prefixing the name with $ (e.g., $var). Alternatively,
# if necessary to set them off from surrounding text, they can also be wrapped with curly braces (e.g., ${var}).

# This example compares a simple template with similar string interpolation using the % operator and the new format
# string syntax using str.format()

values = {"var": "foo"}

t = string.Template("""
Variable: $var
Escape: $$
Variable in text: ${var}sity""")

print("TEMPLATE", t.substitute(values))

s = """
Variable: %(var)s
Escape: %%
Variable in text: %(var)siable"""

print("INTERPOLATION", s % values)

f = """
Variable: {var}
Escape: {{}}
Variable in text: {var}iable"""

print("FORMAT", s.format(**values))

# In the first two cases, the trigger character ($ or %) is escaped by repeating it twice. For the format syntax,
# both { and } need to be escaped by repeating them.

# One key difference between templates and string interpolation or formatting is that the type of the arguments is not
# taken into account. The values are converted to strings, and the strings are inserted into the result. No formatting
# options are available. For example, there is no way to control the number of digits used to represent a floating-point
# value.
# A benefit, though, is that use of the safe_substitute() method makes it possible to avoid exceptions if not all of the
# values needed by the template are provided as arguments.

t = string.Template("$var is here but $missing is not provided")

try:
    print("substitute()     :", t.substitute(values))
except KeyError as err:
    print("ERROR:", str(err))

print("safe_substitute()    :", t.safe_substitute(values))

"""Advanced Templates"""
# The default syntax for string.Template can be changed by adjusting the regular expression patterns it uses to find the
# variable names in the template body. A simple way to do that is to change the delimiter and idpattern class attributes


class MyTemplate(string.Template):
    delimiter = "%"
    idpattern = "[a-z]+_[a-z]+"


template_text = """
Delimited   : %%
Replaced    : %with_underscore
Ignored     : %notunderscored"""

d = {
    "with_underscore": "replaced",
    "notunderscored": "not replaced",
}

t = MyTemplate(template_text)
print("Modified ID pattern")
print(t.safe_substitute(d))

# In this example, the substitution rules are changed so that the delimiter is % instead of $ and variable names must
# include an underscore somewhere in the middle


# For even more complex changes, it is possible to overide the pattern attribute and define an eentierly new regex.
# The pattern provided must contain four named groups for capturing the escaped delimited, the named variable, a braced
# version of the variable name, and invalid delimited patterns:

t = string.Template("$var")
print(t.pattern.pattern)

# This examples defines a new pattern to create a new type of template, using {{var}} as the varialbe syntax


class NewPattern(string.Template):
    delimiter = "{{"
    pattern = r"""
    \{\{(?:
    (?P<escaped>\{\{)|
    (?P<named>[_a-z][_a-z0-9]*)\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)\}\}|
    (?P<invalid>)
    )
    """


t = NewPattern("""
{{{{
{{var}}
""")

print("MATCHES:", t.pattern.findall(t.template))
print("SUBSTITUTED:", t.safe_substitute(var="replacement"))


""" Constants """

# The string module includes a number of constants related to ASCII and numerical character sets.

import inspect

def is_str(value):
    return isinstance(value, str)

for name, value in inspect.getmembers(string, is_str):
    if name.startswith("_"):
        continue
    print("%s=%r\n" % (name, value))