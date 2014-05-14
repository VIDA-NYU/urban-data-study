import sys
import regex
import os.path
import re

def detect_type(sample_path, output_path, city, id):
  filename = sample_path + "/" + city + "_" + id + ".txt"
  if not os.path.isfile(filename):
    return

  output_detail_file = output_path + "/" + city + "_" + id + ".txt"
#  output_detail_file = "detail_type/" + city + "_" + id + ".txt"

  if os.path.isfile(output_detail_file):
    print "File " + output_detail_file + " is existed"
    return

  output = open(output_detail_file, "w")
  types = {}
  for t in regex.Type:
    types[t] = 0
  with open(filename) as lines:
    for line in lines:
      a = line.strip("\n").split("\t")
      if len(a) < 1:
        continue
      column = a[0]
      values = a[1:]
      type = regex.detect(column, values)
      if len(type) > 0:
        for t in type:
          output.write(column + "\t" + t + "\n")
  output.close()

def main(argv):
  '''
  First Argument: path to directory containing sampling values of all data sets
  Second Argument: path to the file containing all data set ids.
  Third Argument: path to directory containing detection results.
  Fourth Argument: city name, which is used as a prefix for output files.
  '''
  if len(argv) != 4:
    print "The program takes 4 arguments, " + str(len(argv)) + " is given."
    return
  sample_path = argv[0]
  ids_file = argv[1]
  output_path = argv[2]
  city = argv[3]

  with open(ids_file) as lines:
      for line in lines:
        id = line.strip("\n")
        detect_type(sample_path, output_path, city, id)

if __name__=="__main__":
  main(sys.argv[1:])
