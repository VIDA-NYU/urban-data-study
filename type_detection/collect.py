###############################################################################
##
## Copyright (C) 2014, New York University.
## All rights reserved.
## Contact: kien.pham@nyu.edu
##
## "Redistribution and use in source and binary forms, with or without 
## modification, are permitted provided that the following conditions are met:
##
##  - Redistributions of source code must retain the above copyright notice, 
##    this list of conditions and the following disclaimer.
##  - Redistributions in binary form must reproduce the above copyright 
##    notice, this list of conditions and the following disclaimer in the 
##    documentation and/or other materials provided with the distribution.
##  - Neither the name of New York University nor the names of its 
##    contributors may be used to endorse or promote products derived from 
##    this software without specific prior written permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
## THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
## PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
## EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
## PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
## OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
## WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
## OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
###############################################################################

import sys
import re
from os import walk
import os.path

def get_size(ids_path, json_path, city):
  '''
  Goal: get the number of datasets
  ids_path: path to directory containing list of data set ids
  json_path: path to directory containing all json files
  '''
  n = 0
  ids_file =  ids_path + "/" + city + "_ids.txt" 
  with open(ids_file) as lines:
    for line in lines:
      id = line.strip("\n")
      json_file = json_path + "/" + city + "/" + id + ".json"
      if os.path.isfile(json_file):
        n += 1
  print n
  return n

def stat_table(city, detection_path):
  table_count = {"Location":set(), "Time":set(), "Number":set(), "LatLon":set(), "ZipCode":set(), "Address":set(), "Null":set(), "Year":set(), "Month":set(), "Date":set()}
  for (dirpath, dirnames, filenames) in walk(detection_path):
    for filename in filenames:
      filename = detection_path + "/" +  filename
      if re.search(city, filename):
        id = filename[-13:-4]
        with open(filename) as lines:
          for line in lines:
            a = line.strip("\n").split("\t")
            #type = a[0]
            #count = int(a[1])
            #if (count > 0) & (type in table_count):
            type = a[1]
            if type in table_count:
              table_count[type].add(id)
    break
  table_count["Location"] = table_count["LatLon"].union(table_count["ZipCode"].union(table_count["Address"]))
  table_count["Time"] = table_count["Month"].union(table_count["Date"].union(table_count["Year"]))

  return table_count

def generic_type(ids_path, json_path, cities, allcities, filename, detection_path):
  output = open(filename, "w")
  for city in cities:
    n = get_size(ids_path, json_path, city)
    table_count = stat_table(city, detection_path)
    #print str(len(table_count["Location"])/float(n)) + "," + str(len(table_count["Time"])/float(n)) + "," + str(len(table_count["Number"])/float(n)) + "," + str(len(table_count["Null"])/float(n))
    output.write(str(len(table_count["Location"])/float(n)) + "," + str(len(table_count["Time"])/float(n)) + "," + str(len(table_count["Number"])/float(n)) + "," + str(len(table_count["Null"])/float(n)) + "\n")

  n = 0
  loc = 0
  time = 0
  num = 0
  null = 0
  for city in allcities:
    n += get_size(ids_path, json_path, city)
    table_count = stat_table(city, detection_path)
    loc += len(table_count["Location"]) 
    time += len(table_count["Time"]) 
    num += len(table_count["Number"])
    null += len(table_count["Null"])
  #print str(loc/float(n)) + "," + str(time/float(n)) + "," + str(num/float(n)) +  "," + str(null/float(n))
  output.write(str(loc/float(n)) + "," + str(time/float(n)) + "," + str(num/float(n)) +  "," + str(null/float(n)) + "\n")
  output.close()

def location_type(ids_path, json_path, cities, allcities, filename, detection_path):
  output = open(filename, "w")
  for city in cities:
    n = get_size(ids_path, json_path, city)
    table_count = stat_table(city, detection_path)
    #print str(len(table_count["LatLon"])/float(n)) + "," + str(len(table_count["Address"])/float(n)) + "," + str(len(table_count["ZipCode"])/float(n))  
    output.write(str(len(table_count["LatLon"])/float(n)) + "," + str(len(table_count["Address"])/float(n)) + "," + str(len(table_count["ZipCode"])/float(n)) + "\n")

  n = 0
  latlon = 0
  address = 0
  zipcode = 0
  for city in allcities:
    n += get_size(ids_path, json_path, city)
    table_count = stat_table(city, detection_path)
    latlon += len(table_count["LatLon"]) 
    address += len(table_count["Address"]) 
    zipcode += len(table_count["ZipCode"])
  #print str(latlon/float(n)) + "," + str(address/float(n)) + "," + str(zipcode/float(n))
  output.write(str(latlon/float(n)) + "," + str(address/float(n)) + "," + str(zipcode/float(n)) + "\n")
  output.close()

def time_type(ids_path, json_path, cities, allcities, filename, detection_path):
  output = open(filename, "w")
  for city in cities:
    n = get_size(ids_path, json_path, city)
    table_count = stat_table(city, detection_path)
    #print str(len(table_count["Date"])/float(n)) + "," + str(len(table_count["Month"])/float(n)) + "," + str(len(table_count["Year"])/float(n)) 
    output.write(str(len(table_count["Date"])/float(n)) + "," + str(len(table_count["Month"])/float(n)) + "," + str(len(table_count["Year"])/float(n)) + "\n")

  n = 0
  date = 0
  month = 0
  year = 0
  for city in allcities:
    n += get_size(ids_path, json_path, city)
    table_count = stat_table(city, detection_path)
    date += len(table_count["Date"]) 
    month += len(table_count["Month"]) 
    year += len(table_count["Year"])
  #print str(date/float(n)) + "," + str(month/float(n)) + "," + str(year/float(n))
  output.write(str(date/float(n)) + "," + str(month/float(n)) + "," + str(year/float(n)) + "\n")
  output.close()

def main(argv):
  '''
  First argument: filename to save information of generic types
  Second argument: filename to save information of location types
  Third argument: filename to save information of time types
  '''
  if len(argv) != 6:
    print "The program takes 6 arguments, " + str(len(argv)) + " is given."
    return
  
  generic_file = argv[0]
  location_file = argv[1]
  time_file = argv[2]
  ids_path = argv[3]
  json_path = argv[4]
  detection_path = argv[5]
  cities = ["nyc", "kcmo", "seattle", "chicago", "baltimore", "sf", "raleigh", "edmonton", "boston", "austin"]
  allcities = ["nyc", "kcmo", "seattle", "chicago", "baltimore", "sf", "raleigh", "edmonton", "boston", "austin"
              "deleon", "madison", "honolulu", "nola", "oaklandnet", "slc", "somervillema", "weatherford", "wellington"]
  cities = ["austin"]          
  allcities = ["austin"]          
  #print "generic"
  generic_type(ids_path, json_path, cities, allcities, generic_file, detection_path)
  #print "location"
  location_type(ids_path, json_path, cities, allcities, location_file, detection_path)
  #print "time"
  time_type(ids_path, json_path, cities, allcities, time_file, detection_path)
  
if __name__=="__main__":
  main(sys.argv[1:])
