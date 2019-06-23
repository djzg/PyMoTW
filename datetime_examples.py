#!/usr/bin/env/python3

""" datetime - Date and Time value manipulation """

# datetime contains functions and classes for working with dates and times, separately and together


""" Times """

# Time values are represented with the time class. A time instance has attributes for hour, minute, second and
# microsecond and can also include time zone information.

import datetime

t = datetime.time(1, 2, 3)

print(t)
print('hour       :', t.hour)
print('minute     :', t.minute)
print('second     :', t.second)
print('microsecond:', t.microsecond)
print('tzinfo     :', t.tzinfo)
print()

# The arguments to initialize a tim einstance are optional, but the default of 0 is unlikely to be correct.

# A time instance only holds values of time, and not a date associated with the time.

print("Earliest     :", datetime.time.min)
print("Latest       :", datetime.time.max)
print("Resolution   :", datetime.time.resolution)
print()
# The min and max class attributes reflect the valid range of times in a single day.

# The resolution for time is limited to whole microseconds

for m in [1, 0, 0.1, 0.6]:
    try:
        print("{:02.1f}:".format(m),
              datetime.time(0, 0, 0, microsecond=m))
    except TypeError as err:
        print("ERROR:", err)
print()
# Floating point values for microseconds cause a TypeError


""" Dates """

# Calendar date values are represented with the date class. Instances have attributes for year, month, and day. It is
# easy to create a date representing the current date using the today() class method.

today = datetime.date.today()

print(today)

print("ctime:", today.ctime())
tt = today.timetuple()

print("tuple:  tm_year = ", tt.tm_year)
print("         tm_mon = ", tt.tm_mon)
print("        tm_mday = ", tt.tm_mday)
print("        tm_hour = ", tt.tm_hour)
print("         tm_min = ", tt.tm_min)
print("         tm_sec = ", tt.tm_sec)
print("        tm_wday = ", tt.tm_wday)
print("        tm_yday = ", tt.tm_yday)
print("       tm_isdst = ", tt.tm_isdst)
print("ordinal  :", today.toordinal())
print("Year     :", today.year)
print("Month    :", today.month)
print("Day      :", today.day)
print()
# This example prints the current date in several formats.

# There are also class methods for creating instances from POSIX timestamps or integers representing date values from
# the Gregorian calendar, where January 1 of the year 1 is 1 and each subsequent day increments the value by 1.


import datetime
import time

o = 733114
print("o                :", o)
print("fromordinal(o)   :", datetime.date.fromordinal(o))

t = time.time()
print("t                :", t)
print("fromtimestamp(t) :", datetime.date.fromtimestamp(t))

print()

# As with time, the range of date values supported can be determined using the min and max attributes.


print('Earliest  :', datetime.date.min)
print('Latest    :', datetime.date.max)
print('Resolution:', datetime.date.resolution)
print()

# The resolution for dates is whole days.


# Another way to create new date instances uses the replace() method of an existing date.

d1 = datetime.date(2019, 6, 23)
print("d1:", d1.ctime())

d2 = d1.replace(year=2021)
print("d2:", d2.ctime())

print()

""" timedeltas """


# Future and past dates can be calculated using basic arithmetic on two datetime objects, or by combining a datetime
# with a timedelta. Subtracting dates produces a timedelta, and a timedelta can be added or subtracted from a date to
# produce another date. The internal value for a timedelta are stored in days, seconds, and microseconds.

print("microseconds :", datetime.timedelta(microseconds=1))
print("milliseconds :", datetime.timedelta(milliseconds=1))
print("seconds      :", datetime.timedelta(seconds=1))
print("minutes      :", datetime.timedelta(minutes=1))
print("hours        :", datetime.timedelta(hours=1))
print("days         :", datetime.timedelta(days=1))
print("weeks        :", datetime.timedelta(weeks=1))
print()

# Intermediate level values passed to the constructor are converted into days, seconds, and microseconds.

# The full duration of a timedelta can be retrieved as a number of seconds using total_seconds()

for delta in [datetime.timedelta(microseconds=1),
              datetime.timedelta(milliseconds=1),
              datetime.timedelta(seconds=1),
              datetime.timedelta(minutes=1),
              datetime.timedelta(hours=1),
              datetime.timedelta(days=1),
              datetime.timedelta(weeks=1)]:
    print("{:15} = {:8} seconds".format(
        str(delta), delta.total_seconds()
    ))
print()
# The return value is a floating point number, to accommodate sub-second durations.


""" Date arithmetic """

# Date math uses the standard arithmetic operators.

today = datetime.date.today()
print("Today:", today)

one_day = datetime.timedelta(days=1)
print("One day:", one_day)

yesterday = today - one_day
print("Yesterday:", yesterday)

tomorrow = today + one_day
print("Tomorrow:", tomorrow)

print()
print("tomorrow-yesterday:", tomorrow - yesterday)
print("yesterday-tomorrow:", yesterday - tomorrow)
print()

# This example with date objects illustrates using timedelta objects to compute new dates, and subtracting date
# instances to produce timedeltas (including a negative delta value).

# A timedelta object also supports arithmetic with integers, floats, and other timedelta instances.

print('1 day    :', one_day)
print('5 days   :', one_day * 5)
print('1.5 days :', one_day * 1.5)
print('1/4 day  :', one_day / 4)

# assume an hour for lunch
work_day = datetime.timedelta(hours=7)
meeting_length = datetime.timedelta(hours=1)
print("meetings per day:", work_day / meeting_length)
print()
# In this example, several multiples of a single day are computed, with the resulting timedelta holding the appropriate
# number of days or hours. The final example demonstrates how to compute values by combining two timedelta objects.
# In this case, the result is a floating point number.


""" Comparing values """

# Both date and time value scan be compared using the standard comparison operators to determine which is earlier or
# later.

print('Times:')
t1 = datetime.time(12, 55, 0)
print('  t1:', t1)
t2 = datetime.time(13, 5, 0)
print('  t2:', t2)
print('  t1 < t2:', t1 < t2)

print()
print('Dates:')
d1 = datetime.date.today()
print('  d1:', d1)
d2 = datetime.date.today() + datetime.timedelta(days=1)
print('  d2:', d2)
print('  d1 > d2:', d1 > d2)
print()

""" Combining dates and times """

# Use the datetime class to hold values consisting of both date and time components. As with date, there are several
# convenient class methods to make creating datetime instances from other common values.

print('Now    :', datetime.datetime.now())
print('Today  :', datetime.datetime.today())
print('UTC Now:', datetime.datetime.utcnow())
print()

FIELDS = [
    "year", "month", "day",
    "hour", "minute", "second",
    "microsecond",
]

d = datetime.datetime.now()
for attr in FIELDS:
    print("{:15}: {}".format(attr, getattr(d, attr)))
print()

# The datetime instance has all of the attributes of both a date and a time object

# Just as with date, datetime provides convenient class methods for creating new instances. It also includes
# fromordinal() and fromtimestamp().

t = datetime.time(1, 2, 3)
print('t :', t)

d = datetime.date.today()
print('d :', d)

dt = datetime.datetime.combine(d, t)
print('dt:', dt)

print()


""" Formatting and parsing """

# The default string representation of datetime object uses the ISO-8601 format. Alternate formats can be generated
# using strftime().

format = "%a %b %d %H:%M:%S %Y"

today = datetime.datetime.today()

print("ISO:", today)

s = today.strftime(format)
print("strftime:", s)

d = datetime.datetime.strptime(s, format)
print("strptime:", d.strftime(format))
print()
# Use datetime.strptime() to convert formatted strings to datetime instances.

# The same formatting can be used with Python's string formatting mini-language by placing them after the ":" in the
# field specification of the format string.

today = datetime.datetime.today()
print('ISO     :', today)
print('format(): {:%a %b %d %H:%M:%S %Y}'.format(today))

# Each datetime format code must still be prefixed with %, and subsequent colons are treated as literal characters
# to include in the output

"""
Symbol 	Meaning 	Example
%a 	Abbreviated weekday name 	'Wed'
%A 	Full weekday name 	'Wednesday'
%w 	Weekday number – 0 (Sunday) through 6 (Saturday) 	'3'
%d 	Day of the month (zero padded) 	'13'
%b 	Abbreviated month name 	'Jan'
%B 	Full month name 	'January'
%m 	Month of the year 	'01'
%y 	Year without century 	'16'
%Y 	Year with century 	'2016'
%H 	Hour from 24-hour clock 	'17'
%I 	Hour from 12-hour clock 	'05'
%p 	AM/PM 	'PM'
%M 	Minutes 	'00'
%S 	Seconds 	'00'
%f 	Microseconds 	'000000'
%z 	UTC offset for time zone-aware objects 	'-0500'
%Z 	Time Zone name 	'EST'
%j 	Day of the year 	'013'
%W 	Week of the year 	'02'
%c 	Date and time representation for the current locale 	'Wed Jan 13 17:00:00 2016'
%x 	Date representation for the current locale 	'01/13/16'
%X 	Time representation for the current locale 	'17:00:00'
%% 	A literal % character 	'%'
"""


""" Time zones """

# Within datetime, time zones are represented by subclasses of tzinfo. Since tzinfo is an abstract base class,
# applications need to define a subclass and provide appropriate implementations for a few methods to make it useful.

# datetime does include a somewhat naive implementation in the class timezone that uses a fixed offset from UTC, and
# does not support different offset values on different days of the year, such as where daylight saving time applies,
# or where the offset from UTC has changed over time.

print()

min6 = datetime.timezone(datetime.timedelta(hours=-6))
plus6 = datetime.timezone(datetime.timedelta(hours=6))
d = datetime.datetime.now(min6)

print(min6, ":", d)
print(datetime.timezone.utc, ":",
      d.astimezone(datetime.timezone.utc))
print(plus6, ":", d.astimezone(plus6))

# convert to the current system timezone
d_system = d.astimezone()
print(d_system.tzinfo, ":", d_system)

# To convert a datetime value from one time zone to another, use astimezone(). In the example above, two separate
# time zones 6 hours on either side of UTC are shown, and the utc instance from datetime.timezone is also used for
# reference. The final output line shows the value in the system timezone, acquired by calling astimezone() with no
# argument.

# Note
# The third party module pytz is a better implementation for time zones. It supports named time zones, and the offset
# database is kept up to date as changes are made by political bodies around the world.
