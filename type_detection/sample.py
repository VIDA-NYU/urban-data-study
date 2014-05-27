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
import ijson
import os.path
import re

def get_schema(filename):
  '''
  Extract column names of a given dataset from JSON file
  '''
  schema = []
  schema_set = set()
  try:
    if filename[-4:]=='json':
      count = 0
      with open(filename) as lines:
        for line in lines:
          if re.search("\"data\" :", line) is None:
            if line[-2] == ',':
              kv = line.strip("\n ,").split(" : ")
              if len(kv)==2:
                k = kv[0].strip("\"")
                v = kv[1].strip("\"")
                if k=="fieldName":
                  count += 1
                  if count>8:
                    if v not in schema_set:
                      schema.append(v)
                      schema_set.add(v)
          else:
            break
    else:
      print filename + ' is not JSON file'
  except Exception as ex:
    print ex
    print "Error line: " + str(sys.exc_traceback.tb_lineno)
  return schema

def is_none(item):
  '''
  Check if an object is None or list of None items
  '''
  if item == None:
    return True
  if type(item) == list:
    for e in item:
      if e != None:
        return False
    return True
  else:
    return False

def tostr(obj):
  '''
  Convert an object to string, lower case and remove end line characters
  '''
  if type(obj) is unicode:
    return obj.encode('utf-8').replace("\n", "").lower()
  else:
    return str(obj).replace("\n", " ").lower()

def sample(data_path, id, output_path, city, max, MAX):
  filename = data_path + "/" + id + ".json"
  if not os.path.isfile(filename):
    return

  output_file = output_path + "/" + city + "_" + id + ".txt"
  if os.path.isfile(output_file):
    print "File " + output_file + " is existed."
    return
  output = open(output_file, "w")
  schema = get_schema(filename)
  
  count = 0
  item = []
  try:
    filehandle = open(filename)
    data = ijson.items(filehandle, "data.item")
    values_list = []
    for atb in schema:
      values_list.append([atb])
    for item in data:
      count += 1
      if count == MAX:
        break
      item = item[8:]
      if count == 1: #only do this once
        values_list = values_list[0:len(item)]
      for i in range(len(item)):
        if (len(values_list[i])<max):
          if (is_none(item[i]) != True):
            values_list[i].append(tostr(item[i]))
          is_done = False
      if is_done:
        break
      else:
        is_done = True
    #Write the sampling values to file
    for values in values_list:
      line = values[0] #First value is the atribute name
      for value in values[1:]:
        line += "\t" + value
      output.write(line + "\n")

    output.close()
  except Exception as e:
    print e

def main(argv):
  '''
  First Argument: path to directory containing all JSON files of a given city
  Second Argument: path to the file containing all dataset ids.
  Third Argument: path to directory containing sampling results.
  Fourth Argument: city name, which is used as a prefix for output files.
  '''
  if len(argv) != 4:
    print "The program takes 4 arguments, " + str(len(argv)) + " is given."
    return
  data_path = argv[0]
  ids_file = argv[1]
  output_path = argv[2]
  city = argv[3]
  max = 100 #Maximum number sampling values
  MAX = 10000 #Maximum number of values which are considered for sampling
  try:
    with open(ids_file) as lines:
      for line in lines:
        id = line.strip("\n")
        sample(data_path, id, output_path, city, max, MAX)
  except Exception as e:
    print e
if __name__=="__main__":
  main(sys.argv[1:])
