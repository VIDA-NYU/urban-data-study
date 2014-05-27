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

#!/usr/bin/python
# -*- coding: utf-8 -*-
#Input:
#1) url, i.e: http://data.austintexas.gov
#2) output path
#Get number of datasets, metadata (name, description, tags) and schema using following APIs:
#url + /api/views.json?count=True: COUNT
#url + /api/views.json?limit=200&page=1: METADATA
#url + /api/views/ + datasetid + .json: SCHEMA

import json
import urllib
import codecs
import sys
import os.path

def loadIDs(outpath):
  #Input
  filepath = outpath + '/metadata.csv'
  if not os.path.isfile(filepath):
    return set()
  ids = set([])
  with open(filepath) as f:
    for line in f:
      _array = line.split('\t')
      ids.add(_array[0])
  print 'Done loading IDs'
  return ids

def main(argv):
  url = argv[0] #input
  city = argv[1]
  outpath = argv[2] #output
  #Get the number of datasets
  urlhandle = urllib.urlopen(url + '/api/views.json?count=True')
  content = urlhandle.read()
  js = json.loads(content)
  count = js['count']

  #Output
  meta_f = codecs.open(outpath + '/' + city + '_metadata.csv', 'a', 'utf-8')
  tag_f = codecs.open(outpath + '/' + city + '_tags.csv', 'a', 'utf-8')
  schema_f = codecs.open(outpath + '/' + city + '_schema.csv', 'a', 'utf-8')
  id_tag_f = codecs.open(outpath + '/' + city + '_id_tag.csv', 'a', 'utf-8')
  id_downloadcount_f = codecs.open(outpath + '/' + city + '_id_downloadcount.csv', 'a', 'utf-8')
  id_viewcount_f = codecs.open(outpath + '/' + city + '_id_viewcount.csv', 'a', 'utf-8')
  
  #Load id of the datasets whose metadatas were already retrieved
  ids = loadIDs(outpath)

  #Get metadata of the all datasets
  #Metadata for one dataset is formated in one line. Each attribute value is seperated by tab character and empty value is replaced by the string 'Null'
  print 'Total: ' + str(count)
  pages = count/200 + 1 #total number of pages
  
  for i in range(1, pages+1):
    sys.stdout.write('Getting data from page ' + str(i) + ' ... ')
    urlhandle = urllib.urlopen(url + "/api/views.json?limit=200&page=" + str(i))

    content = urlhandle.read()
    js = json.loads(content)
    for j in range(0, len(js)):
      #Check whether the metadata was already retrieved
      _id = js[j]['id']
      if _id in ids:
        continue
        
      #Get metadata of each dataset
      #ID and NAME
      id = js[j]['id']
      meta = id + '\t' + js[j]['name']
      
      #DESCRIPTION
      if js[j].has_key('description'):
        meta_f.write(meta + "\t" + js[j]['description'].replace('\n', ' ') + "\n")
      #else:
      #  meta_f.write(meta + '\t' + 'null\n')

      #View count
      if js[j].has_key('viewCount'):
        id_viewcount_f.write(id + "\t" +  str(js[j]["viewCount"]) + "\n")
      else:
        id_viewcounnt_f.write(id + "\tnull\n")
      
      #Download count
      if js[j].has_key('downloadCount'):
        id_downloadcount_f.write(id + "\t" +  str(js[j]["downloadCount"]) + "\n")
      else:
        id_downloadcount_f.write(id + "\tnull\n")

      #TAGS
      tag  = ''
      if js[j].has_key('tags'):
        for t in js[j]['tags']:
          tag_f.write(t + '\n')
          tag = tag + ' ' + t
        id_tag_f.write(id + "\t" + tag + "\n")
      else:
        id_tag_f.write(id + "\tnull\n")
    
      #Get schema of each dataset
      schemaurl = url + "/api/views/" + js[j]['id'] + '.json'
      aJS = json.loads(urllib.urlopen(schemaurl).read())
      if aJS.has_key('columns'):
        schema_js = aJS['columns']
        schema = js[j]['id']
        if schema_js != None:
          for field in schema_js:
            schema = schema + '\t' + field['fieldName']
          schema_f.write(schema + '\n')
      else:
        print js[j]['id']
      
    print 'Done'
  print 'Done'
  meta_f.close()
  tag_f.close()
  schema_f.close()
  id_tag_f.close()
  id_downloadcount_f.close()
  id_viewcount_f.close()  

if __name__ == "__main__":
  main(sys.argv[1:])
