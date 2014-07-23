import matplotlib.pyplot as plt
import sys
from os import walk
import re
import datetime
import os.path
from matplotlib.ticker import AutoMinorLocator

def add_date(filename, date2count):
  with open(filename) as lines:
    for line in lines:
      id, pdate, cdate = line.strip("\n").split("\t")
      date = datetime.datetime.fromtimestamp(int(pdate)) #only use publication date
      if date.month < 10:
        month = "0" + str(date.month)
      else:
        month = str(date.month)
      year_month = str(date.year) + month
      if year_month not in date2count:
        date2count[year_month] = 1
      else:
        date2count[year_month] += 1
  return date2count
        
def prepare_data(path):
  date2count = {} #mapping between date and number of datasets
  for (dirpath, dirnames, filenames) in walk(path):
    for filename in filenames:
      if re.search("id_date", filename):
        print path + filename
        date2count = add_date(path + filename, date2count)
    break
  print date2count
  out = open("date2count.csv", "w")
  for date in date2count.keys():
    out.write(date + "\t" + str(date2count[date]) + "\n")
  out.close()

def get_data(path):
  if not os.path.isfile("date2count.csv"):
    prepare_data(path)
  
  date_count = []
  with open("date2count.csv") as lines:
    for line in lines:
      ym, count = line.strip("\n").split("\t")
      date_count.append([ym, count])
  date_count.sort(key=lambda x: x[0])
  return date_count

def main(argv):
  date_count = get_data("../metadata/data/")
  idx = 0
  dates = []
  area = []
  radius = []
  s = 0
  for (date, count) in date_count:
    idx += 1
    s += int(count)
    if (idx%12==0):
      #radius.append(idx)
  #    date = date[:4] + "/" + date[4:]
      date = date[:4]
    else:
      date = ""
    if (idx%6==0):
      radius.append(idx)
      dates.append(date)
      area.append(s)

  #minorLocator = AutoMinorLocator()
  #fig, ax = plt.subplots()
  #ax.xaxis.set_minor_locator(minorLocator)
  #plt.tick_params(which='major', length=8)
  #plt.tick_params(which='minor', length=4, color='r')

  plt.xticks(radius, dates)
#  plt.xticks(rotation=50)
  plt.plot(radius, area)
  plt.xlabel('Timeline')
  plt.ylabel('Number of tables')
  #plt.title('Title here')
  plt.grid()
  plt.show()

if __name__=="__main__":
  main(sys.argv[1:])
