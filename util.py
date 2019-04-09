# Miscellaneous utility functions

from datetime import date, datetime

# replace year of raw results by defaultYear 
# (assuming admission timeline for each program is more or less stable, only month and day matter)
# HAS TO BE A LEAP YEAR
defaultYear = 2000

# cmp function that sorts date by academic year in US, NOT the standard chronological one
# i.e. Sept, Oct, Nov, Dec, Jan, ..., Aug
def academicYearSort(date1, date2):
	today = date.today()
	date1, date2 = date1.date().replace(year=defaultYear), date2.date().replace(year=defaultYear)
	if date1 <= datetime(defaultYear, 8, 31).date() and date2 > datetime(defaultYear, 8, 31).date():
		return 1
	elif date1 > datetime(defaultYear, 8, 31).date() and date2 <= datetime(defaultYear, 8, 31).date():
		return -1
	elif date1 == date2:
		return 0
	elif date1 < date2:
		return -1
	else:
		return 1

# sortResultsByTime:
# given a list of admission results (tuples, the first element is a datetime object)
# returns sorted admission results by time (ascending)
def sortResultsByTime(dates):
	return sorted(dates, key=lambda date: date[0], cmp=academicYearSort)
