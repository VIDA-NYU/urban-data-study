import sys
from os import walk

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

def main(argv):
  city = sys.argv[1]
  schema_file = "../metadata/data/" + city + "_schema.csv" #input
  type_file = "../type_detection/" + city + "/id_att_type.csv" #input
  id_index_file = open(city + "/id_zipcode_index.csv", "w") #output

  mypath = 
  for (dirpath, dirnames, filenames) in walk(mypath):
    
    break
  id2schema = getSchema(schema_file)
  with open(type_file) as lines:
    for line in lines:
      a = line.strip("\n").split("\t")
      pre_item = ""
      id = a[0]
      newline = id
      for item in a:
        if item == "ZipCode":
          column_name = pre_item
          id = a[0]
          schema = id2schema[id]		
          idx = getIndex(id, column_name, schema)
          if idx != -1:
            newline += "\t" + column_name + "\t" + str(idx)
        pre_item = item
      if newline != id:
        id_index_file.write(newline + "\n")
  id_index_file.close()

if __name__=="__main__":
  main(sys.argv[1:])
