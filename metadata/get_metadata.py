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

def loadIDs(outpath):
	#Input
	filepath = outpath + '/metadata.all.csv'
	
	ids = set([])
	with open(filepath) as f:
		for line in f:
			_array = line.split('\t')
			ids.add(_array[0])
	print 'Done loading IDs'
	return ids

def main(argv):
	url = argv[0] #input
	outpath = argv[1] #output
	#Get the number of datasets
	urlhandle = urllib.urlopen(url + '/api/views.json?count=True')
	content = urlhandle.read()
	js = json.loads(content)
	count = js['count']

	#Output
	meta_f = codecs.open(outpath + '/metadata.all.csv', 'a', 'utf-8')
	tag_f = codecs.open(outpath + '/tags.csv', 'a', 'utf-8')
	schema_f = codecs.open(outpath + '/schema.all.csv', 'a', 'utf-8')
        id_tag_f = codecs.open(outpath + '/id_tag.csv', 'a', 'utf-8')
        id_downloadcount_f = codecs.open(outpath + '/id_downloadcount.csv', 'a', 'utf-8')
        id_viewcount_f = codecs.open(outpath + '/id_viewcount.csv', 'a', 'utf-8')
	
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
			else:
				meta_f.write(meta + '\t' + 'null\n')

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
