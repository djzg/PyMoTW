#!/usr/bin/env/python3

""" calendar - Work with dates """

# The calendar module defines the Calendar class, which encapsulates calculations for values such as the dates of the
# weeks in a given month or year. In addition, the TextCalendar and HTMLCalendar classes can produce pre-formatted
# output.

""" Formatting examples """

# The prmonth() method is a simple function that produces the formatted text output for a month.

import calendar

c = calendar.TextCalendar(calendar.MONDAY)
c.prmonth(2019, 7)
print()
# The example configures TextCalendar to start weeks on Monday.

# A similar HTML table can be produrced with HTMLCalendar and formatmonth(). The rendered output looks roughly the same
# but it is wrapped with HTML tags. Each table cell has a class attribute corresponding to the day of the week, so the
# HTML can be styled thorugh CSS.

# To produce output in a format other than the one of the available defaults, use calendar to calculate the dates and
# organize the values into week and month ranges, then iterate over the result. The weekheader(), monthcalendar() and
# yeardays2calendar() methods of Calendar are especially useful for that.

# Calling yearsdays2calendar() produces a sequence of "month row" lists. Each list includes the months as another list
# of weeks. The weeks are lists of tuples made up of day number (1-31) and weekday number (0-6). Days that fall outside
# of the month have a day number of 0.

import pprint

cal = calendar.Calendar(calendar.MONDAY)
cal_data = cal.yeardays2calendar(2019, 7)
print("len(cal_data) : ", len(cal_data))

top_months = cal_data[0]
print("len(top_months) :", len(top_months))

first_month = top_months[0]
print("len(first_month):", len(first_month))

print("first_month:")
pprint.pprint(first_month, width=65)
print()
# Calling yeardays2calendar(2019, 7) returns data for 2019, organized with three months per row

# This is equivalent to the data used by formatyear()

cal = calendar.TextCalendar(calendar.MONDAY)
print(cal.formatyear(2019, 2, 1, 1, 3))


""" Locales """

# To produces a calendar formatted for a locale other than the current defualt, use LocaleTextCalendar or
# LocaleHTMLCalendar

c = calendar.LocaleTextCalendar(locale="croatian")
c.prmonth(2019, 8)
print()

c = calendar.LocaleTextCalendar(locale="fr_FR")
#c.prmonth(2019, 9)

# The first day of the week is not part of the locale settings, and the value is taken from the argument ot the calendar
# class just as with the regular TextCalendar.


""" Calculating dates """

# Although the calendar module focuess mostly on printing full calendars in various formats, it also provides functions
# useful for working with dates in other ways, such as calculating dates for a recurring event.
# To calculate the dates for the meetings for a year, use the return value of monthcalendar()

pprint.pprint(calendar.monthcalendar(2019, 7))

# Some days have a 0 value. Those are days of the week that overlap with the given month but that are part of another
# month.

# To calculate the group meeting dates for a year, assuming they are always on the second Thursday every month, look
# at the output monthcalendar() to find dates on which Thursdays fall. The first and last week of the month are padded
# with 0 values as placeholders.

import sys
year = int(sys.argv[1])

# show every month
for month in range(1, 13):
    # compute the dates for each week that overlaps the month
    c = calendar.monthcalendar(year, month)
    first_week = c[0]
    second_week = c[1]
    third_week = c[2]

    # if there is a Thursday in the first week, the second Thursday is in the second week.
    # Otherwise, the second Tursday must be in third week.
    if first_week[calendar.THURSDAY]:
        meeting_date = second_week[calendar.THURSDAY]
    else:
        meeting_date = third_week[calendar.THURSDAY]

    print(" {:>3}: {:>2}".format(calendar.month_abbr[month],
                           meeting_date))