# Plot admission timeline using results fetched from getAdmissionStats

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import collections, calendar
from datetime import date, timedelta, datetime

import util
from getAdmissionStats import getAdmissionStats

# getTimelineByDecision:
# given a list of result dictionaries
# return a dictionary that groups decision dates by decision type
def getTimelineByDecision(results):
  tlDict = {
    "Accepted": [],
    "Rejected": [],
    "Interview": [],
    "Waitlisted": [],
    "Other": []
  }

  for res in results:
    decision = res['Decision']
    if decision not in tlDict: continue
    tlDict[decision] += [res['Date']]

  return tlDict

# daterange:
# given start date (date object) and end date (date object)
# yields all dates between start and end dates (inclusive)
def daterange(startDate, endDate):
  for n in range(int((endDate - startDate).days)+1):
    yield startDate + timedelta(n)

# fillMissingTime:
# given (1) a list of tuples <date (datetime object), number of decisions (int)>
#       (2) a start month (int)
#       (3) an end month (int)
# returns a list of tuples <datetime objects, number of decisions> 
# with all dates between start and end months (inclusive)
# if the date is associated with some number of decisions in input, the original tuple is preserved
# otherwise it is associated with zero by default
def fillMissingTime(dates, startMonth, endMonth):
  today = date.today()
  startDate, endDate = date(util.defaultYear, startMonth, 1), \
                       date(util.defaultYear, endMonth, calendar.monthrange(util.defaultYear, endMonth)[1])
  if endDate < startDate:                                       # dates wrapped around (e.g. start from Dec, end in April)
    startDate = startDate.replace(year=startDate.year - 1)      # sort of a hack for dates to wrap around
    for i in range(len(dates)):                                 # modify the dummy year value in results from previous calendar year, but same academic year          
      d = dates[i]
      if d[0] >= datetime(util.defaultYear, 9, 1):              # only those between Sept and Dec are affected by academic vs. calendar year
        tmp = d[0].date().replace(year=startDate.year)
        if tmp >= startDate and tmp <= endDate: dates[i] = (datetime(tmp.year, tmp.month, tmp.day), d[1])
  dates = [d for d in dates if d[0].date() >= startDate and d[0].date() <= endDate]
  datesOnly = [d[0] for d in dates]
  for singleDate in daterange(startDate, endDate):
    d = datetime(singleDate.year, singleDate.month, singleDate.day)
    if d in datesOnly: continue                                 # date already present in results
    dates.append((d, 0))
  return dates

# accuTimelineByDecision:
# given (1) a <decision type, decision date list> dictionary
#       (2) a start month (int)
#       (3) an end month (int)
# returns a <decision type, decision date list> dictionary
# where the element of each decision date list is a tuple <date (datetime object), total number of decisions up to that date (int)>
# if the date is associated with some number of decisions in input, the original tuple is preserved
# all dates are between the first day of start month and the last day of end month (inclusive)
def accuTimelineByDecision(tlDict, startMonth, endMonth):
  accuDict = {}

  for decision in tlDict:
    c = collections.Counter(tlDict[decision])                   # count number of decisions made on each date with Gradcafe results entry
    accuDict[decision] = util.sortResultsByTime(fillMissingTime(c.items(), startMonth, endMonth))
    dates, counts = [x[0] for x in accuDict[decision]], [x[1] for x in accuDict[decision]] 
    dates = matplotlib.dates.date2num(dates)                    # Convert datetime object to maplotlib format
    counts = [sum(counts[:i+1]) for i in range(len(counts))]    # python 2.7 doesn't have accumulate in itertools... sad
    accuDict[decision] = sorted(zip(dates, counts), key=lambda x: x[0])
  return accuDict

# plotAllTimeLines:
# given (1) a <decision type, decision date list> dictionary of aggregated number of decisions over time
#       (2) a optional list of decision types (string)
# plots timeline of aggregated number of results of specified type of decisions
# if no decision type is specified (i.e. None), all relevant decisions (Accepted, Rejected, Interviewed, Waitlisted) will be plotted as separate series
def plotAllTimeLines(accuDict, decisions=None):
  color = {
    "Accepted": 'green',
    "Rejected": 'red',
    "Interview": 'yellow',
    "Waitlisted": 'blue',
    "Other": 'black'
  }
  for decision in accuDict:
    if decision == "Other": continue                            # skip Other; these are not really administration decisions
    if decisions and not decision in decisions: continue
    x, y = [v[0] for v in accuDict[decision]], [v[1] for v in accuDict[decision]]
    plt.plot(x, y, color=color[decision], label=decision)

  ax = plt.gca()
  hfmt = matplotlib.dates.DateFormatter('%b\n%d')               # format dates (abbrev month in word + day number)
  ax.xaxis.set_major_formatter(hfmt)

  plt.xlabel('Date')
  plt.ylabel('Number of Results (aggregated)')
  plt.tight_layout()
  plt.legend()                                                  # show legend
  plt.show()
