#!/usr/bin/env/python3

# The enum module defines an enumeration type with iteration and comparison capabilities. It can be used to create
# well-defined symboles for values, instead of using literal integers or strings.

""" Creating Enumerations """

# A new enumeration is defined using the class syntax by sublcassing Enum and adding class attributes describing the values.

import enum


class BugStatus(enum.Enum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1


print("\nMember name: {}".format(BugStatus.wont_fix.name))
print("\nMember value: {}".format(BugStatus.wont_fix.value))

# The members of the Enum are converted to instances as the class is parsed. Each instance hags a name property
# corresponding to the member name and a value property corresponding to the value assigned to the name in the class
# definition.


""" Iteration """

# Iterating over the enum class produces the individual members of the enumeration

for status in BugStatus:
    print("{:20} = {:10}".format(status.name, status.value))


""" Comparing Enums """

# Because enumeration members are not ordered, they support only comparison by identity and equality.

actual_state = BugStatus.wont_fix
desired_state = BugStatus.fix_released

print("Equality:",
      actual_state == desired_state,
      actual_state == BugStatus.wont_fix)
print("Identity:",
      actual_state is desired_state,
      actual_state is BugStatus.wont_fix)
print("Ordered by value:")
# The < and > comparison operators raise TypeError exceptions:
try:
    print("\n".join(" " + s.name for s in sorted(BugStatus)))
except TypeError as err:
    print("  Cannot sort: {}".format(err))

# Use the IntEnum class for enumerations where the members need to behave more like numbers - eg. to support comparisons


class BugStatus(enum.IntEnum):
    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1


print('Ordered by value:')
print('\n'.join('  ' + s.name for s in sorted(BugStatus)))


""" Unique enumeration values """

# Enum members with the same value are tracked as alias references to the same member object. Aliases do not cause
# repeated values to be present in the iterator for the Enum


class BugStatus(enum.Enum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1

    by_design = 4
    closed = 1


for status in BugStatus:
    print('{:15} = {}'.format(status.name, status.value))

# Because by_design and closed are aliases for other members, they do not appear separately in the output
# when iterating over Enum.
print('\nSame: by_design is wont_fix: ',
      BugStatus.by_design is BugStatus.wont_fix)
print('Same: closed is fix_released: ',
      BugStatus.closed is BugStatus.fix_released)

# To require all members to have unique values, add the @unique decorator to the Enum.


#@enum.unique
class BugStatus(enum.Enum):

    new = 7
    incomplete = 6
    invalid = 5
    wont_fix = 4
    in_progress = 3
    fix_committed = 2
    fix_released = 1

    # This will trigger an error with unique applied.
    by_design = 4
    closed = 1

# Members with repeated values trigger a ValueError exception when the Enum class is being interpreted



""" Creating Enumerations programmatically """

# In some cases, it is more convenient to create enumerations programmatically, rather than hard-coding them in a
# class definition. For those situations, Enum also supports passing the member names and values to the class constructor

BugStatus = enum.Enum(
    value="BugStatus",
    names=("fix_released fix_committed in_progress wont_fix invalid incomplete new"),
    )

print("Member: {}".format(BugStatus.new))

print("\n  All members:")
for status in BugStatus:
    print("{:15} = {}".format(status.name, status.value))

# For more control over the values associated with members, the names string can be replaced with a sequence of two-part
# tuples or a dictionary mapping names to values.

# In this example, a list of two-part tuples is given instead of a single string containing only the member names.
# This makes it possible to reconstruct the BugStatus enumeration with the members in the same order as the version defined.
BugStatus = enum.Enum(
    value="BugStatus",
    names=[
        ("new", 7),
        ("incomplete", 6),
        ("wont_fix", 4),
        ("in_progress", 3),
        ("fix_committed", 2),
        ("fix_released", 1),
    ],
)

print("  All members:")
for status in BugStatus:
    print("{:20} = {}".format(status.name, status.value))


""" Non-integer Member values """

# Enum member values are not erstricted to integers. In fact, any type of object can be associated with a member.
# If the value is a tuple, the members are passed as individual arguments to __init__()


class BugStatus(enum.Enum):

    new = (7, ['incomplete',
               'invalid',
               'wont_fix',
               'in_progress'])
    incomplete = (6, ['new', 'wont_fix'])
    invalid = (5, ['new'])
    wont_fix = (4, ['new'])
    in_progress = (3, ['new', 'fix_committed'])
    fix_committed = (2, ['in_progress', 'fix_released'])
    fix_released = (1, ['new'])

    def __init__(self, num, transitions):
        self.num = num
        self.transitions = transitions

    def can_transition(self, new_state):
        return new_state.name in self.transitions

# In this example each member value is a tuple containing the numerical ID and a list of valid transitions away from
# the current state

print()
print("Name:", BugStatus.in_progress)
print("Value:", BugStatus.in_progress.value)
print("Custom attribute:", BugStatus.in_progress.transitions)
print("Using attribute:", BugStatus.in_progress.can_transition(BugStatus.new))
print()
# For more complex cases, tuples might become unwieldy. Since member values can be any type of object, dictionaries
# can be used for cases where there are a lot of separate attributes to track for each enum value.
# Complex values are passed directly to __init__() as the only argument other than self.


# This example expresses the same data as the previous example, using dictionaries rather than tuples.
class BugStatus(enum.Enum):

    new = {
        'num': 7,
        'transitions': [
            'incomplete',
            'invalid',
            'wont_fix',
            'in_progress',
        ],
    }
    incomplete = {
        'num': 6,
        'transitions': ['new', 'wont_fix'],
    }
    invalid = {
        'num': 5,
        'transitions': ['new'],
    }
    wont_fix = {
        'num': 4,
        'transitions': ['new'],
    }
    in_progress = {
        'num': 3,
        'transitions': ['new', 'fix_committed'],
    }
    fix_committed = {
        'num': 2,
        'transitions': ['in_progress', 'fix_released'],
    }
    fix_released = {
        'num': 1,
        'transitions': ['new'],
    }

    def __init__(self, vals):
        self.num = vals['num']
        self.transitions = vals['transitions']

    def can_transition(self, new_state):
        return new_state.name in self.transitions


print('Name:', BugStatus.in_progress)
print('Value:', BugStatus.in_progress.value)
print('Custom attribute:', BugStatus.in_progress.transitions)
print('Using attribute:',
      BugStatus.in_progress.can_transition(BugStatus.new))
