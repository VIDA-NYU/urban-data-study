# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import json
import sys
import ijson
import codecs
import re

def get_zipcode(f):
	global id2index
	with open(f) as lines:
		for line in lines:
			a = line.strip("\n").split("\t")
			id = a[0]
			index_list = []
			for i in range(1,len(a)):
				if i%2 == 0:
					index_list.append(int(a[i]))
			if id2index.has_key(id):
				id2index[id][0] = index_list
			else:	
				id2index[id] = [index_list, [], []] #first list contains zipcode, second list contains latlon, third list contains time

def get_latlon(f):
	global id2index
	lat = ["latitude", "x", "lat_dd_wgs84", "location_x", "centroidx", "coordinates", "lat", "location", "_lit_lat", "_south", "stop_lat", "building_latitude", "centroid_latitude", "intptlat", "intptlat10", "xpos", "_47_564727820", "x"]
	lon = ["longitude", "y", "lon_dd_wgs84", "location_y", "centroidy", "coordinates", "lon", "location", "_lit_lon", "_west", "stop_lon", "building_longitude", "centroid_longitude", "intptlon", "intptlat10", "ypos", "_122_363840492", "y"]
	with open(f) as lines:
		for line in lines:
			a = line.strip("\n").split("\t")
			id = a[0]
			index_list = [-1, -1] #first element is lat, second one is lon
			pre_item = "" #
			for i in range(1,len(a)):
				if (index_list[0] != -1) & (index_list[1] != -1): #if we already found latitude and longitude index => stop checking
					break
				if pre_item == "":
					if a[i] in lat :
						pre_item = "latitude"
						continue
					if a[i] in lon:
						pre_item = "longitude"
						continue
				if pre_item == "latitude":
					index_list[0] = int(a[i])
					pre_item = ""
					continue
				if pre_item == "longitude":
					index_list[1] = int(a[i])
					pre_item = ""
					continue
					
			if (index_list[0] != -1) & (index_list[1] != -1):
				if id2index.has_key(id):
					id2index[id][1] = index_list
				else:	
					id2index[id] = [[], index_list, []] #first list contains zipcode, second list contains latlon, third list contains time



def get_data(city, id):
	global id2index
	#Open files
	zipcode_f = open(city + "/" + id + "-zipcode.csv", "w")
	latlon_f = open(city + "/" + id + "-latlon.csv", "w")

	#Initialize sets. Set contains distinct values
	zipcode_set = []
	latlon_set = []

	index = id2index[id]
	zipcode_index = index[0]
	latlon_index = index[1]

	content = open("../download/" + city + "/" + id + ".json")
	data = ijson.items(content, 'data.item')
	Zipcode = re.compile('([\d]{5})')
	try:
		for item in data:
			item = item[8:]
			if len(zipcode_index) > 0: #If there is zipcode attribute
				for i in zipcode_index:#for each dataset, there could be more than row containing zipcode
					if item[i]: #if value is not None
						match_zipcode = Zipcode.search(str(item[i]))
                                                if match_zipcode:
                                                        zipcode = match_zipcode.group(1)
                                                        zipcode_set.append(zipcode)
			elif len(latlon_index) == 2: #if there are lat/lon attributes
				lat = item[latlon_index[0]]
				lon = item[latlon_index[1]]
				if (lat != None) & (lon != None): # if values are not None
					latlon = lat + "," + lon
					latlon_set.append(latlon)
	except:
		print id + "\tException"
	#Write to file
	if len(zipcode_set) > 0:
		for item in zipcode_set:
			try:
				zipcode_f.write(item + "\n")
			except:
				print id + "\tException"
				continue
	if len(latlon_set) > 0:
		for item in latlon_set:
			try:
				latlon_f.write(item + "\n")		
			except:
				print id + "\tException"
				continue
	zipcode_f.close()
	latlon_f.close()

city = sys.argv[1]
zipcode_f = city + "/id_zipcode_index.csv"
latlon_f = city + "/id_latlon_index.csv"

#GLOBAL variable
id2index = {} #Each id is mapped to 3 lists. first list contains zipcode, second list contains latlon, third list contains time

get_zipcode(zipcode_f)
get_latlon(latlon_f)
for id in id2index:
	get_data(city, id)
