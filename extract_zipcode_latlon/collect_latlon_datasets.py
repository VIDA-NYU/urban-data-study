import sys

def getSchema(f):
	id2schema = {}
	with open(f) as lines:
		for line in lines:
			a = line.strip("\n").split("\t")
			id = a[0]
			schema = a[1:]
			id2schema[id] = schema
	return id2schema

def getIndex(id, column_name, schema):
	idx = -1
	for column in schema:
		idx += 1
		if column == column_name:
			return idx
	return -1

def getIDlist(f):
	l = set()
	with open(f) as lines:
		for line in lines:
			a = line.split("\t")
			id = a[0]
			l.add(id)
	return l

city = sys.argv[1]
schema_f = "../metadata/" + city + "/schema.csv" #input
zipcode_f = city + "/id_zipcode_index.csv" #input, list of datasets that contain zipcode attribute
type_f = "../type-detector-noclusters/" + city + "/id_att_type.csv" #input
id_index_f = open(city + "/id_latlon_index.csv", "w") #output

id2schema = getSchema(schema_f)
zipcodelist = getIDlist(zipcode_f) #list of datasets that contain zipcode attribute
with open(type_f) as lines:
	for line in lines:
		a = line.strip("\n").split("\t")
		pre_item = ""
		id = a[0]
		if id in zipcodelist:
			continue
		newline = id
		for item in a:
			if item == "LatLon":
				column_name = pre_item
				schema = id2schema[id]		
				idx = getIndex(id, column_name, schema)
				if idx != -1:
					newline += "\t" + column_name + "\t" + str(idx)
			pre_item = item
		if newline != id:
			id_index_f.write(newline + "\n")
id_index_f.close()
