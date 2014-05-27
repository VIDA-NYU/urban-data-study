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
sys.path.append('../lib/')
from os import walk
import re

#Extract the schema from json
#Compute the jaccard similarity between schema

def preprocess(fieldName):
  return fieldName.lower().replace(' ', '_')

def get_schema(filepath):
  print filepath
  schema = []
  try:
    if filepath[-4:]=='json':
      count = 0
      with open(filepath) as lines: 
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
                    schema.append(v)
          else:
            break
    else:
      print filepath + ' is not json file'
  except Exception as ex:
    print ex
    print "Error line: " + str(sys.exc_traceback.tb_lineno)
  return schema

def get_all_schema(path):
  m = {} #Map between id and schema
  try:
    for (dirpath, dirnames, filenames) in walk(path):
      for filename in filenames:
        if filename[-4:] == 'json':
          id = filename[:-5]
          schema = get_schema(dirpath + filename)
          if schema:
            m[id] = schema
      break
    return m
  except Exception as ex:
    print ex
    return None

  return m

def jaccard_similarity(schema1, schema2):
  return len(schema1.intersection(schema2))/float(len(schema1.union(schema2)))

def run(city, in_path, out_path):
  f = open(out_path + "/" + city + "_schema_similarity.txt", "w")
  m = get_all_schema(in_path)
  ids = m.keys()
  for i in range(len(ids)):
    for j in range(i+1, len(ids)):
      sim = jaccard_similarity(set(m[ids[i]]), set(m[ids[j]]))
      if (sim>0):
        f.write(ids[i] + "\t" + ids[j] + "\t" + str(sim) + "\n")
  f.close()      

def main(argv):
  if len(argv) != 3:
    print "The program takes 3 arguments, " + str(len(argv)) + " is given."
    return
  city = argv[0]
  in_path = argv[1] + "/"
  out_path = argv[2] 
  #path = "data/"
  run(city, in_path, out_path)

if __name__=="__main__":
  main(sys.argv[1:])
