import re
# -*- coding: utf-8 -*-

def get_zipcode():
  zips = set()
  data = open("zipcode.txt").read()
  lines = data.split("\n")
  for line in lines:
    a = line.split(", ")
    a = a[1:] #The first item is city name
    for zip in a:
      zips.add(zip)
  return zips

def is_number(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

max = 100 #number of sampling values for each attribute

Type = ["Date", "Year", "Month",
        "LatLon", "ZipCode", "Address", 
        "Number",  "Null"]

Address = "(street)|(boulevard)|(avenue)|(drive)|(place)|(road)|(st)|(ave)|(rd)|(pkwy)|(blvd)" 
#Address = "(street)|(boulevard)|(avenue)|(drive)|(place)|(road)|(ave)|(pkwy)|(blvd)" 
ZipCode = re.compile("(^|\D+)(\d{5})($|\D+)")
zips = get_zipcode()

Null = set(["null", "none", "unspecified", "na", "n/a"])

LatLon = re.compile(u'(^|\D+)(\(?[news]?[+-]?(([1][0-2][1-9])|(0?[2345789][\d]))\.[\d]{5,16}°?[news]?\)?)') #remove ^ and $ from the above regex. This regex matches: [ null, "40.754943122337956", "-73.97258640397098", null, false ]
#USA latitude is from 20-49, longitude is from 70-129, except Honolulu and Alaska
#\D matches everything but not number

#Day = set(["mon", "tue", "wed", "thu", "fri", "sat", "sun"])
Month = set(["jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"])

Year = re.compile('(^|\D+)(\d{4})($|\D+)')
Years = set()
for y in range(1900, 2020):
  Years.add(str(y))

Date = re.compile('[0-2][\d]:[0-6][\d]:[0-6][\d]')
#Date = re.compile('([1-2][09][\d][\d][^0-9][0-1][\d][^0-9][0-3][\d])|([0-1][\d][^0-9][0-3][\d][^0-9][1-2][09][\d][\d])')

#REGULAR EXPRESSION TO MATCH COLUMN NAME:
ZIPCODE = re.compile("zip")
LATLON = re.compile("latitude|longitude")
ADDRESS = re.compile("address")
DATE = re.compile("date")
YEAR = re.compile("^year$")
MONTH = re.compile("^month$")
#DAY = re.compile("day")

def detect(column, values):
  if len(values) == 0:
    return ["Null"]
  column = column.strip(" \t").lower()
  for i in range(len(values)):
    values[i] = values[i].strip(" \t")
  if isNull(column, values):
    return ["Null"]

  res = []
  if isDate(column, values):
    res.append("Date")
  if isMonth(column, values):
    res.append("Month")
  if isYear(column, values):
    res.append("Year")
#  if isDay(column, values):
#    return "Day"

  if isLatLon(column, values):
    res.append("LatLon")
  if isZipCode(column, values):
    res.append("ZipCode")
  if isAddress(column, values):
    res.append("Address")

  if isNumber(column, values):
    res.append("Number")
  return res

def isDate(column, values):
  #if re.search("date", column):
  if DATE.search(column):
    return True

  count = 0
  for value in values: 
    if Date.search(value):
      	count += 1

  if count > len(values)*0.8:
    return True
  else:
    return False

def isYear(column, values):
  #if re.search("year", column):
  if YEAR.search(column):
    return True

  count = 0
  for v in values:
    #match = re.search("(^|\D+)(\d{4})($|\D+)", v)
    match = Year.search(v)
    if match:
      y = match.group(2)
      if y in Years:
        count += 1

  if count > (len(values)*0.8):
    return True
  else:
    return False

def isMonth(column, values):
  #if re.search("month", column):
  if MONTH.search(column):
    return True

  count = 0
  for v in values:
    if v in Month:
      count += 1

  if count > (len(values)*0.8):
    return True
  else:
    return False

def isDay(column, values):
  #if re.search("day", column):
  if DAY.search(column):
    return True

  count = 0
  for v in values:
    if v in Day:
      count += 1

  if count > (len(values)*0.8):
    return True
  else:
    return False

def isLatLon(column, values):
  #if re.search("(latitude)|(longitude)", column):
  if LATLON.search(column):
    return True
  count = 0
  for value in values:
    #value = "_" + value
    if LatLon.search(value):
      count += 1
  if count > len(values)*0.8:
      return True
  else:
      return False

def isZipCode(column, values):
  #zips = get_zipcode()

  #if re.search("zip", column):
  if ZIPCODE.search(column):
    return True

  count = 0
  for v in values:
    #match = re.search("\d{5}", v)
    match = ZipCode.search(v)
    if match:
      zip = match.group(2)
      if zip in zips:
        count += 1
  if count > len(values)/2:#Zip code could be from other cities so the threshold 0.5 should be ok
    return True
  else:
    return False

def contain_number(s):
    #contain number at the begining of string
    if re.search("^\d+", s):
      return True
    else:
      return False
    #return any(i.isdigit() for i in s) 

def isAddress(column, values):
  #if re.search("address", column):
  if ADDRESS.search(column):
    return True

  count = 0
  for v in values:
    if re.search(Address, v):
      if contain_number(v):
        if ' ' in v:
          count += 1
  if count > len(values)/2:
    return True
  else:
    return False

def isNumber(column, values):
  for v in values:
    if not is_number(v):
      return False
  return True
  '''
  count = 0
  for v in values:
    if is_number(v):
      count +=1
  if count > 0.8*len(values):
    return True
  '''
def isNull(column, values):
  for v in values:
    if v not in Null:
      return False
  return True
