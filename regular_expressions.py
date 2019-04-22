#!/usr/bin/env/python3

""" Finding patterns in text """

import re

pattern = "this"
text = "Does this text match the pattern?"

match = re.search(pattern, text)

s = match.start()
e = match.end()
print('Found "{}\nin "{}\nfrom {} to {} ("{}")'.format(
    match.re.pattern, match.string, s, e, text[s:e]))

# The start() and end() methods give the indexes into the string showing where the text matched by the pattern occurs.


""" Compiling expressions """

regexes = [
    re.compile(p)
    for p in ["this", "that"]
]
text = "Does this text match the pattern?"

print("Text: {!r}\n".format(text))

for regex in regexes:
    print('Seeking "{}" ->'.format(regex.pattern),
          end=" ")
    if regex.search(text):
        print("match!")
    else:
        print("no match")


""" Multiple matches """

# The findall() function returns all of the substrings of the input that match the pattern without overlapping

text = "abbaaabbbbaababaa"
pattern = "ab"

for match in re.findall(pattern, text):
    print("Found {!r}".format(match))

# The finditer() function returns an iterator that produces Match instances instead of the strings returned by findall()

for match in re.finditer(pattern, text):
    s = match.start()
    e = match.end()
    print("Found {!r} at {:d}:{:d}".format(
        text[s:e], s, e))


""" Pattern syntax """


def test_patterns(text, patterns):
    """Given source text and a list of patterns, look for
    matches for each pattern within the text and print
    them to stdout
    """
    for pattern, desc in patterns:
        print("'{}' ({})\n".format(pattern, desc))
        print("   '{}'".format(text))
        for match in re.finditer(pattern, text):
            s = match.start()
            e = match.end()
            substr = text[s:e]
            n_backslashes = text[:s].count('\\')
            prefix = "." * (s + n_backslashes)
            print("    {}'{}'".format(prefix, substr))
        print()
    return


if __name__ == "__main__":
    test_patterns("abbaaabbbbaaaaa",
                  [("ab", "'a' followed by 'b'"),
                   ])


""" Repetition """
# There are five ways to express repetition in a pattern. A pattern followed by the meta-character * is repeated zero
# or more times (allowing a pattern to repeat zero times means it does not need to appear at all to match). If the * is
# replaced with +, the pattern must appear at least once. Using ? means the pattern appears zero or one time. For a
# specific number of occurrences, use {m} after the pattern, where m is the number of times the pattern should repeat.
# Finally, to allow a variable but limited number of repetitions, use {m,n}, where m is the minimum number of
# repetitions and n is the maximum. Leaving out n ({m,}) means the value must appear at least m times, with no maximum.

test_patterns(
    'abbaabbba',
    [('ab*', 'a followed by zero or more b'),
     ('ab+', 'a followed by one or more b'),
     ('ab?', 'a followed by zero or one b'),
     ('ab{3}', 'a followed by three b'),
     ('ab{2,3}', 'a followed by two to three b')],
)

# Greediness can be turned off by following the repetition instruction with ?.

test_patterns(
    'abbaabbba',
    [('ab*?', 'a followed by zero or more b'),
     ('ab+?', 'a followed by one or more b'),
     ('ab??', 'a followed by zero or one b'),
     ('ab{3}?', 'a followed by three b'),
     ('ab{2,3}?', 'a followed by two to three b')],
)


""" Character sets """
# A character set is a group of characters, any one of which can match at that point in the pattern.
# For example, [ab] would match either a or b

test_patterns(
    'abbaabbba',
    [('[ab]', 'either a or b'),
     ('a[ab]+', 'a followed by 1 or more a or b'), # this pattern will consume the entire string
     ('a[ab]+?', 'a followed by 1 or more a or b, not greedy')], # non greedy form of the previous pattern
)

# A character set can also be used to exclude specific characters. The carat (^) means to look for characters that
# are not in the set following the carat


test_patterns(
    'This is some text -- with punctuation.',
    [('[^-. ]+', 'sequences without -, ., or space')],
)

# A more compact format using character ranges can be used to define a character set to include all of the contiguous
# characters between the specified start and stop points

test_patterns(
    'This is some text -- with punctuation.',
    [('[a-z]+', 'sequences of lowercase letters'),
     ('[A-Z]+', 'sequences of uppercase letters'),
     ('[a-zA-Z]+', 'sequences of letters of either case'),
     ('[A-Z][a-z]+', 'one uppercase followed by lowercase')],
)

# As a special case of a character set, the meta-character dot, or period (.), indicates that the pattern should match
# any single character in that position.

test_patterns(
    'abbaabbba',
    [('a.', 'a followed by any one character'),
     ('b.', 'b followed by any one character'),
     ('a.*b', 'a followed by anything, ending in b'),
     ('a.*?b', 'a followed by anything, ending in b')],
)

""" Escape codes """
# The escape codes recognized by re are listed in the table:
# \d - a digit
# \D - a non-digit
# \s - whitespace(tab, space, newline, etc.)
# \S - non-whitespace
# \w - alphanumeric
# \W - non-alphanumeric

test_patterns(
    'A prime #1 example!',
    [(r'\d+', 'sequence of digits'),
     (r'\D+', 'sequence of non-digits'),
     (r'\s+', 'sequence of whitespace'),
     (r'\S+', 'sequence of non-whitespace'),
     (r'\w+', 'alphanumeric characters'),
     (r'\W+', 'non-alphanumeric')],
)

# To match the characters that are part of the regex syntax, escape the characters in the search pattern.

test_patterns(
    r'\d+ \D+ \s+',
    [(r'\\.\+', 'escape code')],
)

""" Anchoring """
# In addition to describing the content of a pattern to match, the relative location can be specified in the input text
# where the pattern should appear by using anchoring instructions. The table below lists valid anchoring codes:
#
# ^ - start of string, or line
# $ - end of string, or line
# \A - start of string
# \Z - end of string
# \b - empty string at the beginning or end of a word
# \B - empty string not at the beginning or end of a word

test_patterns(
    'This is some text -- with punctuation.',
    [(r'^\w+', 'word at start of string'),
     (r'\A\w+', 'word at start of string'),
     (r'\w+\S*$', 'word near end of string'),
     (r'\w+\S*\Z', 'word near end of string'),
     (r'\w*t\w*', 'word containing t'),
     (r'\bt\w+', 't at start of word'),
     (r'\w+t\b', 't at end of word'),
     (r'\Bt\B', 't, not start or end of word')],
)

""" Constraining the search """
# If the pattern must appear at the front of the input, then using match() instead of search() will anchor the search
# without having to explicitly include an anchor in the search pattern.

text = "This is some text -- with punctuation."
pattern = "is"

print("Text     :", text)
print("Pattern  :", pattern)

# Since the literal text "is" does not appear at the start of the input text, it is not found using match().
m = re.match(pattern, text)
print("Match    :", m)
# The sequence appears two other times in the text, so search() finds it.
s = re.search(pattern, text)
print("Search   :", s)

# The fullmatch() method requires that the entier input string match the pattern.
text = 'This is some text -- with punctuation.'
pattern = 'is'

print('Text       :', text)
print('Pattern    :', pattern)

m = re.search(pattern, text)
print('Search     :', m)
s = re.fullmatch(pattern, text)
print('Full match :', s)

# The search() method of a complied regex accepts optional start and end position parameters to limit the search to
# a substring of the input.

text = "This is some text -- with punctuation."
pattern = re.compile(r'\b\w*is\w*\b')

print("Text:", text)
print()

pos = 0
while True:
    match = pattern.search(text, pos)
    if not match:
        break
    s = match.start()
    e = match.end()
    print("   {:>2d}  :  {:>2d} = '{}'".format(
        s, e - 1, text[s:e]
    ))
    # Move forward in text for the next search
    pos = e

""" Dissecting matches with groups """
# Searching for pattern matches is the basis of the powerful capabilities provided by regular expressions.
# Adding groups to a pattern isolates parts of the matching text, expanding those capabilities to create a parser.
# Groups are defined by enclosing patterns in parentheses.

test_patterns(
    'abbaaabbbbaaaaa',
    [('a(ab)', 'a followed by literal ab'),
     ('a(a*b*)', 'a followed by 0-n a and 0-n b'),
     ('a(ab)*', 'a followed by 0-n ab'),
     ('a(ab)+', 'a followed by 1-n ab')],
)

# To access the substrings matched by the individual groups within a pattern, use the groups() method of the Match object.

text = "This is some text -- with punctuation."

print(text)
print()

patterns = [
    (r'^(\w+)', "word at start of string"),
    (r'(\w+)\S*$', "word at the end, with optional punctuation"),
    (r'(\bt\w+)\W+(\w+)', "word starting with t, another word"),
    (r'(\w+t)\b', "word ending with t")
]

# match.groups() returns a sequence of strings in the order of the groups within the expression that matches the string
for pattern, desc in patterns:
    regex = re.compile(pattern)
    match = regex.search(text)
    print("'{}' ({})\n".format(pattern, desc))
    print("   ", match.groups())
    print()

# To ask for the match of a single group, use the group() method.

text = 'This is some text -- with punctuation.'

print('Input text            :', text)

# word starting with 't' then another word
regex = re.compile(r'(\bt\w+)\W+(\w+)')
print('Pattern               :', regex.pattern)

match = regex.search(text)
print('Entire match          :', match.group(0))
print('Word starting with "t":', match.group(1))
print('Word after "t" word   :', match.group(2))

# Python extends the basic grouping syntax to add named groups. To set the name of a group, use (?P<name>pattern).


text = 'This is some text -- with punctuation.'

print(text)
print()

patterns = [
    r'^(?P<first_word>\w+)',
    r'(?P<last_word>\w+)\S*$',
    r'(?P<t_word>\bt\w+)\W+(?P<other_word>\w+)',
    r'(?P<ends_with_t>\w+t)\b',
]

for pattern in patterns:
    regex = re.compile(pattern)
    match = regex.search(text)
    print("'{}'".format(pattern))
    print('  ', match.groups())
    print('  ', match.groupdict())
    print()

# Use groupdict() to retrieve the dictionary mapping group names to substrings from the match. Named patterns are
# included in the ordered sequence returned by groups() as well.

# An updated version of test_patterns() that shows the numbered and named groups matched by a pattern will make the
# following examples easier to follow.

def test_patterns(text, patterns):
    """Given source text and a list of patterns, look for
    matches for each pattern within the text and print them to stdout
    """

    for pattern, desc in patterns:
        print("{!r} ({})\n".format(pattern, desc))
        print("  {!r}".format(text))
        for match in re.finditer(pattern, text):
            s = match.start()
            e = match.end()
            prefix = " " * (s)
            print(
                '  {}{!r}{}'.format(prefix, text[s:e], " " * (len(text) - e)),
                end=" ",
            )
            print(match.groups())
            if match.groupdict():
                print("{}{}".format(
                    " " * (len(text) - s),
                    match.groupdict()),
                )
        print()
    return

# Since a group is itself a complete regular expression, groups can be nested within other groups to build even
# more complicated expressions.

# In this case the group (a*) matches an empty string, so the return value from groups() includes that empty string.
test_patterns(
    "abbaabbba",
    [(r'a((a*)(b*))', "a followed by 0-n a and 0-n b ")],
)

# Groups are also useful for specifying alternative patterns. Use the pipe (|) symbol.

test_patterns(
    "abbaabbba",
    [(r'a((a+)|(b+))', "a then seq. of a or seq. of b"),
     (r'a((a|b)+)', "a then seq. of [ab]")],
)

# Defining a group containing a subpattern is also useful in cases where the string matching the subpattern is not part
# of what should be extracted from the full text. These kinds of groups are called non-capturing. Non-capturing groups
# can be used to describe repetition patterns or alternatives, without isolating the matching portion of the string in
# the value returned. To create a non-capturing group, use the syntax (?:pattern).

test_patterns(
    "abbaabbba",
    [(r'a((a+)|(b+))', "capturing form"),
     (r'a((?:a+)|(?:b+))', "noncapturing")]
)



""" Search options """
# Option flags are used to change the way the matching engine processes an expression. The flags can be combined using
# bitwise OR operation, then passed to compile(), search(), match(), and other functions that accept a pattern for searching

# IGNORECASE causes literal characters and character ranges in the pattern to match both uppercase and lowercase characters

text = "This is some text -- with punctuation."
pattern = r'\bT\w+'
with_case = re.compile(pattern)
without_case = re.compile(pattern, re.IGNORECASE)

print("Text:\n {!r}".format(text))
print("Pattern:\n {}".format(pattern))
print("Case-sensitive:")
for match in with_case.findall(text):
    print("   {!r}".format(match))
print("Case-insensitive")
for match in without_case.findall(text):
    print("   {!r}".format(match))

# Two flags affect how searching in multi-line input works: MULTILINE and DOTALL.
# The MULTILINE flag controls how the pattern matching code processes anchoring instruction for text containing newline characters.
# When multiline mode is turned on, the anchor rules for ^ and $ apply at the beginning and end of each line, in addition
# to the entire string.

text = "This is some text -- with punctuation."
pattern = r'(^\w+)|(\w+\S*$)'
single_line = re.compile(pattern)
multiline = re.compile(pattern, re.MULTILINE)

# The pattern in the example matches the first or last word of the input. It matches line at the end of string, even
# though there is no newline.
print('Text:\n  {!r}'.format(text))
print('Pattern:\n  {}'.format(pattern))
print('Single Line :')
for match in single_line.findall(text):
    print('  {!r}'.format(match))
print('Multline    :')
for match in multiline.findall(text):
    print('  {!r}'.format(match))


# DOTALL is the other flag related to multiline text. Normally, the dot character (.) matches everything in the input
# text except a newline character. The flag allows the dot to match newlines as well.

text = "This is some text -- with punctuation.\nA second line."
pattern = r'.+'
no_newlines = re.compile(pattern)
dotall = re.compile(pattern, re.DOTALL)

print('Text:\n  {!r}'.format(text))
print('Pattern:\n  {}'.format(pattern))
print('No newlines :')
for match in no_newlines.findall(text):
    print('  {!r}'.format(match))
print('Dotall      :')
for match in dotall.findall(text):
    print('  {!r}'.format(match))

# ASCII flag

text = u'Français złoty Österreich'
pattern = r'\w+'
ascii_pattern = re.compile(pattern, re.ASCII)
unicode_pattern = re.compile(pattern)

print("Text     :", text)
print("Pattern  :", pattern)
print("ASCII    :", list(ascii_pattern.findall(text)))
print("Unicode  :", list(unicode_pattern.findall(text)))

# VERBOSE mode expressions, which allow comments and extra whitespace to be embedded in the pattern.

address = re.compile(r'[\w\d.+-]+@([\w\d.]+\.)+(com|org|edu)')

candidates = [
    u'first.last@example.com',
    u'first.last+category@gmail.com',
    u'valid-address@mail.example.com',
    u'not-valid@example.foo',
]

for candidate in candidates:
    match = address.search(candidate)
    print("{:<30}   {}".format(
        candidate, "Matches" if match else "No match"
    ))

# Converting the expression to a more verbose format will make it easier to extend

address = re.compile(
    """
    [\w\d.+-]+      # username
    @
    ([\w\d.]+\.)+   # domain name prefix
    (com|org|edu)   # TODO: support more top-level domains
    """,
    re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'first.last+category@gmail.com',
    u'valid-address@mail.example.com',
    u'not-valid@example.foo',
]

for candidate in candidates:
    match = address.search(candidate)
    print("{:<30}  {}".format(
        candidate, "Matches" if match else "No match"),
    )

# This expanded version parses inputs that include a person's name and email address, as might appear in an email header.
# The name comes first and stands on its own, and the email address follows, surrounded by angle brackets (< and >).

address = re.compile(
    """
    # A name is made up of letters, and may include '.' for title abbreviations and middle initials.
    ((?P<name>
        ([\w.,]+\s+)*[\w.,]+)
        \s*
        # Email addresses are wrapped in angle brackets but only if a name is found, so keep the start bracket in this group
        <
    )? # The entire name is optional
     
    # The address itself: username@domain.tld
    (?P<email>
    [\w\d.+-]+      # username
    @
    ([\w\d.]+\.)+   # domain name prefix
    (com|edu|org)   # limit the allowed top-level domains
    )
    >?  # optional closing angle bracket
    """,
    re.VERBOSE)
candidates = [
    u'first.last@example.com',
    u'first.last+category@gmail.com',
    u'valid-address@mail.example.com',
    u'not-valid@example.foo',
    u'First Last <first.last@example.com>',
    u'No Brackets first.last@example.com',
    u'First Last',
    u'First Middle Last <first.last@example.com>',
    u'First M. Last <first.last@example.com>',
    u'<first.last@example.com>',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print('  Name :', match.groupdict()['name'])
        print('  Email:', match.groupdict()['email'])
    else:
        print('  No match')


# In situations where flags cannot be added when compiling an expression, such as when a pattern is passed as an
# argument to a library function that will compile it later, the flags can be embedded inside the expression string iteslf.
# for example, to turn case-insensitive matching on, add (?i) to the beginning of the expression.

text = "This is some text -- with punctuation."
pattern = r'(?i)\bT\w+'
regex = re.compile(pattern)

print('Text      :', text)
print('Pattern   :', pattern)
print('Matches   :', regex.findall(text))

# In many cases, it is useful to match a part of a pattern only if some other part will also match. For example, in the
# email parsing expression, the angle brackets were marked as optional. Realistically, the brackets should be paired,
# and the expression should match only if both are present, or neither is. This modified version of the expression uses
# a positive look ahead assertion to match the pair. The look ahead assertion syntax is (?=pattern).

address = re.compile(
    """
    ((?P<name>
    ([\w.,]+\s+)*[\w.,]+
    )
    \s+
    )   # name is no longer optional
    
    # LOOKAHEAD
    # Email addresses are wrapped in angle brackets, but only
    # if both are present or neither is.
    (?= (<.*>$)     # remainder wrapped in angle brackets
    |
    ([^<].*[^>]$)   # remainder 'not' wrapped in angle brackets
    )
    <?  # optional opening angle bracket
    
    (?P<email>
    [\w\d.+-]+      # username
    @
    ([\w\d.]+\.)+   # domain name prefix
    (com|edu|org)   # limit the allowed top-level domains
    )
    >?  # optional closing angle bracket
    """,
    re.VERBOSE)

candidates = [
    u'First Last <first.last@example.com>',
    u'No Brackets first.last@example.com',
    u'Open Bracket <first.last@example.com',
    u'Close Bracket first.last@example.com>',
]

for cand in candidates:
    print("Candidate:", cand)
    match = address.search(cand)
    if match:
        print(" Name:", match.groupdict()["name"])
        print(" Email:", match.groupdict()["email"])
    else:
        print("No match")


# A negative look ahead assertion ((?!pattern)) says that the pattern does not match the text following the current point
# For example, the email recognition pattern could be modified to ignore the noreply mailing addresses commonly used by
# automated systems

address = re.compile(
    """
    ^
    
    # Ignore noreply addresses
    (?!noreply@.*$)
    
    [\w\d.+-]+      # username
    @
    ([\w\d.]+\.)+   # domain name prefix
    (com|org|edu)   # limit the allowed top-level domains
    
    $
    """,
    re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'noreply@example.com',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print('  Match:', candidate[match.start():match.end()])
    else:
        print('  No match')

# Instead of looking ahead for noreply in the username portion of the email address, the pattern can alternatively be
# written using a negative look behind assertion after the username is matched using the syntax (?<!pattern).

address = re.compile(
    '''
    ^

    # An address: username@domain.tld

    [\w\d.+-]+       # username

    # Ignore noreply addresses
    (?<!noreply)

    @
    ([\w\d.]+\.)+    # domain name prefix
    (com|org|edu)    # limit the allowed top-level domains

    $
    ''',
    re.VERBOSE)

candidates = [
    u'first.last@example.com',
    u'noreply@example.com',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print('  Match:', candidate[match.start():match.end()])
    else:
        print('  No match')

# A positive look behind assertion can be used to find text following a pattern using the syntax (?<=pattern).
# In the following example, the expression finds Twitter handles.

twitter = re.compile(
    """
    # A twitter handle: @username
    (?<=@)
    ([\w\d_]+)      # username
    """,
    re.VERBOSE)

text = "This text includes two Twitter handles. One for @TheDiscovery, and one for the author, @djzg."

print(text)
for match in twitter.findall(text):
    print("Handle:", match)

# Self referencing expressions
# Matched values can be used in later parts of an expression. For example, the email example can be updated to match
# only addresses composed of the first and last names of the person by including back-references to those groups.
# The easiest way to achieve this is by referring to the previously matched group by ID number, using \num.


address = re.compile(
    r'''

    # The regular name
    (\w+)               # first name
    \s+
    (([\w.]+)\s+)?      # optional middle name or initial
    (\w+)               # last name

    \s+

    <

    # The address: first_name.last_name@domain.tld
    (?P<email>
      \1               # first name
      \.
      \4               # last name
      @
      ([\w\d.]+\.)+    # domain name prefix
      (com|org|edu)    # limit the allowed top-level domains
    )

    >
    ''',
    re.VERBOSE | re.IGNORECASE)

candidates = [
    u'First Last <first.last@example.com>',
    u'Different Name <first.last@example.com>',
    u'First Middle Last <first.last@example.com>',
    u'First M. Last <first.last@example.com>',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print('  Match name :', match.group(1), match.group(4))
        print('  Match email:', match.group(5))
    else:
        print('  No match')

# Python’s expression parser includes an extension that uses (?P=name) to refer to the value of a named group matched
# earlier in the expression.

address = re.compile(
    '''

    # The regular name
    (?P<first_name>\w+)
    \s+
    (([\w.]+)\s+)?      # optional middle name or initial
    (?P<last_name>\w+)

    \s+

    <

    # The address: first_name.last_name@domain.tld
    (?P<email>
      (?P=first_name)
      \.
      (?P=last_name)
      @
      ([\w\d.]+\.)+    # domain name prefix
      (com|org|edu)    # limit the allowed top-level domains
    )

    >
    ''',
    re.VERBOSE | re.IGNORECASE)

candidates = [
    u'First Last <first.last@example.com>',
    u'Different Name <first.last@example.com>',
    u'First Middle Last <first.last@example.com>',
    u'First M. Last <first.last@example.com>',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print('  Match name :', match.groupdict()['first_name'],
              end=' ')
        print(match.groupdict()['last_name'])
        print('  Match email:', match.groupdict()['email'])
    else:
        print('  No match')

# The other mechanism for using back-references in expressions chooses a different pattern based on whether a previous
# group matched. The email pattern can be corrected so that the angle brackets are required if a name is present,
# and not required if the email address is by itself. The syntax for testing whether if a group has matched is
# (?(id)yes-expression|no-expression), where id is the group name or number, yes-expression is the pattern to use
# if the group has a value, and no-expression is the pattern to use otherwise.

address = re.compile(
    '''
    ^

    # A name is made up of letters, and may include "."
    # for title abbreviations and middle initials.
    (?P<name>
       ([\w.]+\s+)*[\w.]+
     )?
    \s*

    # Email addresses are wrapped in angle brackets, but
    # only if a name is found.
    (?(name)
      # remainder wrapped in angle brackets because
      # there is a name
      (?P<brackets>(?=(<.*>$)))
      |
      # remainder does not include angle brackets without name
      (?=([^<].*[^>]$))
     )

    # Look for a bracket only if the look-ahead assertion
    # found both of them.
    (?(brackets)<|\s*)

    # The address itself: username@domain.tld
    (?P<email>
      [\w\d.+-]+       # username
      @
      ([\w\d.]+\.)+    # domain name prefix
      (com|org|edu)    # limit the allowed top-level domains
     )

    # Look for a bracket only if the look-ahead assertion
    # found both of them.
    (?(brackets)>|\s*)

    $
    ''',
    re.VERBOSE)

candidates = [
    u'First Last <first.last@example.com>',
    u'No Brackets first.last@example.com',
    u'Open Bracket <first.last@example.com',
    u'Close Bracket first.last@example.com>',
    u'no.brackets@example.com',
]

for candidate in candidates:
    print('Candidate:', candidate)
    match = address.search(candidate)
    if match:
        print('  Match name :', match.groupdict()['name'])
        print('  Match email:', match.groupdict()['email'])
    else:
        print('  No match')

# In addition to searching through text, re supports modifying text using regex as the search mechanism and the
# replacements can reference groups matched in the pattern as part of the substitution text.
# Use sub() to replace all occurrences of a pattern with another string.

bold = re.compile(r'\*{2}(.*?)\*{2}')

text = "Make this **bold**. This **too**."

print("Text:", text)
print("Bold:", bold.sub(r'<b>\1</b>', text))

# Pass a value to count to limit the number of substitutions performed
bold = re.compile(r'\*{2}(.*?)\*{2}')

text = 'Make this **bold**.  This **too**.'

print('Text:', text)
print('Bold:', bold.sub(r'<b>\1</b>', text, count=1))

# subn() works just like sub() except that it returns both the modified string and the count of substitutions made.


bold = re.compile(r'\*{2}(.*?)\*{2}')

text = 'Make this **bold**.  This **too**.'

print('Text:', text)
print('Bold:', bold.subn(r'<b>\1</b>', text))


""" Splitting with patterns """
# str.split() is one of the most frequently used methods for breaking apart strings to parse them. It supports only
# the use of literal values as separators, though, and sometimes a regular expression is necessary if the input is not
# consistently formatted. For example, many plain text markup languages define paragraph separators as two or more
# newline (\n) characters. In this case, str.split() cannot be used because of the “or more” part of the definition.

text = """ Paragraph one
on two lines.

Paragraph two.

Paragraph three."""

for num, para in enumerate(re.findall(r'(.+?)\n{2,}',
                           text,
                           flags=re.DOTALL)):
    print(num, repr(para))
    print()