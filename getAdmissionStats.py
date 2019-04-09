# Get admission statistics
# adapted from https://github.com/utkarshsimha/GradcafeWatcher

import requests
from bs4 import BeautifulSoup
from datetime import date, datetime

import util

# getDecision: 
# given a string encoding the admission decision (assuming standard encoding of raw Gradcafe data)
# returns the actual decision without date (i.e. Accepted/Rejected/Interviewed/Other)
def getDecision(decision):
  tmp = decision.split()
  if tmp[0] == "Wait":   # for some reason gradcafe splits "waitlisted" into "wait listed"...
    return "Waitlisted"
  # assume the first word is the decision, according how decision is encoded by Gradcafe
  return tmp[0]

# getStatus: 
# given a status key string (valid: A/I/U)
# returns the semantic meaning of the status key
def getStatus(key):
  if(key == 'A'):
    return 'American'
  elif(key == 'I'):
    return 'International, w/o US Degree'
  elif(key == 'U'):
    return 'International, w US degree'
  else:
    return 'Unknown({})'.format(key)

# get Date
# given a input string encoding a date (default format on Results page)
# returns the reformatted date
# Specifically, 
# input date format: day(num) month(word) year(num)
# output date format: day(two-digit num) month(abbrev)
def getDate(d, minYear):
  dateFormat = "%d %b %Y"
  tmp = d.split()
  day, month, year = int(tmp[0]), tmp[1], int(tmp[2])      
  if day < 10: day = "0" + str(day)      # if day is a single digit, reformat it to two digits
  if year < minYear: return None
  formatted = "{} {} {}".format(day, month, util.defaultYear)   # add a dummy year value
  return datetime.strptime(formatted, dateFormat)

# getAdmissionStatsByPage:
# given (1) a query url, assuming to be a valid query to Gradcafe Result
#       (2) a page number
#       (3) earliest year of admission results included
#       (3) a list of result dictionaries
# appends to the given list user entries on the given page as dictionaries (returns nothing)
# dictionary structure:
#   College: name of college
#   Program: name of program
#   Decision: admission decision (including interview & other)
#   Status: academic background of user (see getStatus for more info)
#   Date: date the admission result is made (NOT entry submission date)
#   Comments: comment submitted by user along with the admission result
def getAdmissionStatsByPage(url, pageNum, minYear, resList):
  tooFarBack = False
  query = "{}&p={}".format(url,str(pageNum)) # add page number to query string
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
  }
  rawData = requests.get(query, headers=headers).text
  # parse fetched data
  parsedData = BeautifulSoup(rawData, "html.parser")
  # extract actual user entries
  results = parsedData.findAll(attrs={'class':'row0'}) + parsedData.findAll(attrs={'class':'row1'})

  # parse raw results data for relevant info
  for res in results:
      resDict = {}
      tdElements = res.findAll('td')      # get all elements/columns
      resDict['College'] = tdElements[0].get_text()
      resDict['Program'] = tdElements[1].get_text().encode('ascii', 'ignore')
      resDict['Decision'] = getDecision(tdElements[2].get_text().encode('ascii', 'ignore'))
      resDict['Status'] = getStatus(tdElements[3].get_text() ).encode('ascii', 'ignore')
      resDict['Date'] = getDate(tdElements[4].get_text().encode('ascii', 'ignore'), minYear)
      if not resDict['Date']: 
        tooFarBack = True
        break   # entries ordered by date in descending order; can safely ignore the rest
      resDict['Comments'] = tdElements[5].get_text().encode('ascii', 'ignore')
      resList.append(resDict)
  return tooFarBack

# getAdmissionStats:
# given (1) a query url, assuming to be a valid query to Gradcafe Result
#       (2) earliest year of admission results included
# returns a list of user entries as dictionaries returned by the server
# dictionary structure:
#   College: name of college
#   Program: name of program
#   Decision: admission decision (including interview & other)
#   Status: academic background of user (see getStatus for more info)
#   Date: date the admission result is made (NOT entry submission date)
#   Comments: comment submitted by user along with the admission result
def getAdmissionStats(url, minYear):
  # get raw web data from Results page on Gradcafe
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
  }
  resList = []        # list of result entries made by Gradcafe users

  rawData = requests.get(url, headers=headers).text
  # parse fetched data
  parsedData = BeautifulSoup(rawData, "html.parser")
  # get number of pages in total
  numPages = int(parsedData.find(attrs={'class':'admission-search pagination'}).text.split()[4])
  # query each page 
  # (note this means the first page is queried twice; the first query is only to get # of pages - kinda inefficient, but more reusable code)
  for page in range(1,numPages+1):
    if getAdmissionStatsByPage(url, page, minYear, resList): break # entries ordered by date in descending order; can safely ignore the rest

  return resList
