#!/usr/bin/env/python3

""" time - Clock time """

# The time module provides access to several different types of clocks, each useful for different purposes. The standard
# system calls like time() report the system time. The monotonic() clock can be used to measure elapsed time in a long-
# running process because it is guaranteed never to move backwards, even if the system time is changed. For performance
# testing, perf_counter() provides access to the clock with the highest available resolution to make short time
# measurements more accurate. The CPU time is available through clock() and process_time() returns the combined
# processor time and system time.


""" Comparing clocks """

# Implementation details for the clocks varies by platform. Use get_clock_info() to access basic information about the
# current implementation, including the clock's resolution.

import textwrap
import time

available_clocks = [
    ("monotonic", time.monotonic),
    ("perf_counter", time.perf_counter),
    ("process_time", time.process_time),
    ("time", time.time),
]

for clock_name, func in available_clocks:
    print(textwrap.dedent("""\
    {name}:
        adjustable      : {info.adjustable}
        implementation  : {info.implementation}
        monotonic       : {info.monotonic}
        resolution      : {info.resolution}
        current         : {current}
        """).format(
        name=clock_name,
        info=time.get_clock_info(clock_name),
        current=func()
    ))



""" Wall clock time """

# One of the core functions of the time module is time(), which returns the number of seconds since the start of the
# epoch as a floating point value.

print("\nThe time is:", time.time())

# The epoch is the start of measurement for time, which for Unix systems is 0:00 on 01.01.1970. Although the value is
# always a float, actual precision is platform-depentent.

# The float representation is useful when storing or comparing dates, but not as useful for producing human readable
# representations. For logging or printing time ctime() can be more useful.

print("\nThe time is      :", time.ctime())
later = time.time() + 15
print("15 secs from now :", time.ctime(later))

# The second print() call in this example shows how to use ctime() to format a time value other than the current time.


""" Monotonic clocks """

# Because time() looks at the system clock, and the system clock can be changed by the user or system services for
# synchronizing clocks across multiple computers calling time() repeatedly may produce values that go forwards and
# backwards. This can result in unexpected behavior when trying to measure durations or otherwise use those times for
# computations. Avoid those situations by using monotonic(), which always returns values that go forwards.

start = time.monotonic()
time.sleep(0.1)
end = time.monotonic()

print()
print("start    : {:>9.2f}".format(start))
print("end      : {:>9.2f}".format(end))
print("span     : {:>9.5f}".format(end - start))
print()
# The start point for the monotonic clock is not defined, so return walues are only useful for doing calculations with
# other clock values. In this example the duration of the sleep is measured using monotonic().


""" Processor clock time """

# While time() returns a wall clock time, process_time() returns processor clock time. The values returned from
# process_time() reflect the actual time used by the program as it runs.

import hashlib
import time


    # data to use to calculate md5 checksums
data = open(__file__, "rb").read()
for i in range(5):
    h = hashlib.sha1()
    print(time.ctime(), ": {:0.3f} {:0.3f}".format(
        time.time(), time.process_time()
    ))
    for i in range(250000):
        h.update(data)
    cksum = h.digest()

# In this example, the formatted ctime() is printed along with the floating point values from time(), and clock() for
# each iteration through the loop.

# Note
# If you want to run the example on your system, you may have to add more cycles to the inner loop or work with a larger
# amount of data to actually see the difference in times.

# Typically the processor clock does not tick if a program is not doing anything.
print()
template = "{} - {:0.2f} - {:0.2f}"

print(template.format(
    time.ctime(), time.time(), time.process_time()
))

for i in range(3, 0, -1):
    print("Sleeping", i)
    time.sleep(i)
    print(template.format(
        time.ctime(), time.time(), time.process_time()
    ))
print()
# In this example the loop does very little work by going to sleep after each iteration. The time() value increases
# even while the application is asleep, but the process_time() value does not.

# Calling sleep() yields control from the current thread and asks it to wait for the system to wake it back up. If a
# program has only one thread, this effectively blocks the app and it does no work.


""" Performance counter """

# It is important to have a high-resolution monotonic clock for measuring performance. Determining the best clock data
# source requires platform-specific knowledge, which Python provides in perf_counter().

import hashlib
import time

data = open(__file__, "rb").read()

loop_start = time.perf_counter()

for i in range(5):
    iter_start = time.perf_counter()
    h = hashlib.sha1()
    for i in range(200000):
        h.update(data)

    cksum = h.digest()
    now = time.perf_counter()
    loop_elapsed = now - loop_start
    iter_elapsed = now - iter_start
    print(time.ctime(), ": {:0.3f} {:0.3f}".format(
        iter_elapsed, loop_elapsed
    ))
print()
# As with monotonic(), the epoch for perf_counter() is undefined, and the values are meant to be used for comparing and
# computing values, not as absolute times.


""" Time components """

# Storing times as elapsed seconds is useful in some situations, but there are times when a program needs to have access
# to the individual fields of a date (year, month, day). The time module defines struct_time for holding date and time
# values with components broken out so they are easy to access. There are several functions that work with struct_time
# values instead of floats.


def show_struct(s):
    print('  tm_year :', s.tm_year)
    print('  tm_mon  :', s.tm_mon)
    print('  tm_mday :', s.tm_mday)
    print('  tm_hour :', s.tm_hour)
    print('  tm_min  :', s.tm_min)
    print('  tm_sec  :', s.tm_sec)
    print('  tm_wday :', s.tm_wday)
    print('  tm_yday :', s.tm_yday)
    print('  tm_isdst:', s.tm_isdst)

print("gmtime:")
show_struct(time.gmtime())
print("\nlocaltime:")
show_struct(time.localtime())
print("\nmktime:", time.mktime(time.localtime()))

# The gmtime() function returns the current time in UTC.
# localtime() returns the current time with the current time zone applied.
# mktime() takes a struct_time and converts it to the floating point representation.


""" Working with time zones """

# The functions for determining the current time depend on having the time zone set, either by the program or by using
# a default time zone set for the system. Changing the time zone does not change the actual time, just the way it is
# represented.

# To change the time zone, set the environment variable TZ, then call tzset(). The time zone can be specified with a
# lot of detail, right down to the start and stop times for daylight savings time. It is usually easier to use the time
# zone name and let the underlying libraries derive the other information, though.

# this example program changes the time zone to a few different values and shows how the changes affect other settings
# in the time module.

import time
import os
import pytz

def show_zone_info():
    print("TZ       : ", os.environ.get("TZ", "(not set)"))
    print("tzname   :", time.tzname)
    print("Zone     : {} ({})".format(
        time.timezone, (time.timezone / 3600)
    ))
    print("DST      :", time.daylight)
    print("Time     :", time.ctime())
    print()

print("Default:")
show_zone_info()

zones = [
    "GMT",
    "Europe/Zagreb",
    "US/Pacific"
]

for zone in zones:
    os.environ["TZ"] = zone
    pytz.timezone("GMT")
    print(zone, ":")
    show_zone_info()


""" Parsing and formatting times """

# The two functions strptime() and strftime() convert between struct_time and string representations of time values.
# There is a long list of formatting instructions available to support input and output in different styles. Complete
# list is documented in the library documentation for the time module.

# this example converts the current time from a string to a struct_time instance and back to a string.

def show_struct(s):
    print('  tm_year :', s.tm_year)
    print('  tm_mon  :', s.tm_mon)
    print('  tm_mday :', s.tm_mday)
    print('  tm_hour :', s.tm_hour)
    print('  tm_min  :', s.tm_min)
    print('  tm_sec  :', s.tm_sec)
    print('  tm_wday :', s.tm_wday)
    print('  tm_yday :', s.tm_yday)
    print('  tm_isdst:', s.tm_isdst)


now = time.ctime(1483391847.433716)
print("Now", now)

parsed = time.strptime(now)
print("\nParsed:")
show_struct(parsed)

print("\nFormatted:",
      time.strftime("%a %b %d %H:%M:%S %Y", parsed))

# The output string is not exactly like the input, since the day of the month is prefixed with a zero.



