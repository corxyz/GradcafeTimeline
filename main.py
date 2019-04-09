# Main subroutine (cmd tool) to execute the entire pipeline

import argparse

from getAdmissionStats import getAdmissionStats
from plotTimeline import getTimelineByDecision, accuTimelineByDecision, plotAllTimeLines

# initArgs:
# returns a dictionary with all arguments relevant to search query & timeline
def initArgs():
  argDict = {}
  argDict['query'] = ""                     # search query string
  argDict['minYear'] = 2012                 # earliest year from which decision results are included; default to 2012
  argDict['startMonth'] = 9                 # first month to include in timeline; default to September
  argDict['endMonth'] = 8                   # last month to include in timeline; default to August
  argDict['decisions'] = None               # type of decision; default to include all
  return argDict

# parseArgs:
# given (1) a dictionary of initilized arguments
#       (2) argument(s) parsed from command line
# returns a dictionary with arguments updated with command line input
def parseArgs(argDict, args):
  if args.query: argDict['query'] = args.query.replace(" ","+")
  else: raise Exception("Query string must not be empty!")
  if args.minYear: argDict['minYear'] = int(args.minYear)
  if args.start: argDict['startMonth'] = int(args.start)
  if args.end: argDict['endMonth'] = int(args.end)
  if args.decisions: argDict['decisions'] = args.decisions.split()

def main():
  argDict = initArgs()                      # intialize all arguments

  parser = argparse.ArgumentParser()
  parser.add_argument("-q", "--query", help="admission-related search string")
  parser.add_argument("-y", "--minYear", help="earliest year of results")
  parser.add_argument("-s", "--start", help="start month of timeline (academic year)")
  parser.add_argument("-e", "--end", help="end month of timeline (academic year)")
  parser.add_argument("-d", "--decisions", help="type of admission decision")
  args = parser.parse_args()

  parseArgs(argDict, args)                  # parse arguments obtained from command line input
  # default: querying Result page of Gradcafe, displaying 250 results per page
  url = "http://thegradcafe.com/survey/index.php?q={}&pp=250".format(argDict['query'])
  print "Querying {}...\n".format(url) 
  allResults = getAdmissionStats(url, argDict['minYear'])        # get raw results up to a given year
  tld = getTimelineByDecision(allResults)                        # group dates by decision type
  accd = accuTimelineByDecision(tld, argDict['startMonth'], argDict['endMonth'])  # accumulate decisions within the given months
  print "All data fetched.\n"
  plotAllTimeLines(accd, argDict['decisions'])                   # the actual, plotting stuff
  print "Done.\n"

main()
