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
import matplotlib.pyplot as plt
import numpy as np

def getData():
  with open("loc.csv") as lines:
    nn = []
    for line in lines:
      a = line.strip("\n").split(",")
      n = []
      for x in a:
        n.append(float(x))
      nn.append(n)
  m = {}
  m["NYC"] = nn[0]
  m["Kansas"] = nn[1]
  m["Seattle"] = nn[2]
  m["Chicago"] = nn[3]
  m["Baltimore"] = nn[4]
  m["SF"] = nn[5]
  m["Raleigh"] = nn[6]
  m["Edmonton"] = nn[7]
  m["Boston"] = nn[8]
  m["Austin"] = nn[9]
  m["All Cities"] = nn[10]
  s = []
  s.append("NYC")
  s.append("Kansas")
  s.append("Seattle")
  s.append("Chicago")
  s.append("Baltimore")
  s.append("SF")
  s.append("Raleigh")
  s.append("Edmonton")
  s.append("Boston")
  s.append("Austin")
  s.append("All Cities")
  return [s, m]
  

def main(argv):
  s, m = getData()
  label = ["Lat/Lon", "Address", "Zipcode"] #Label for x axis
  _color = {
      "Baltimore":"#a6cee3",
      "Chicago":"#1f78b4",
      "Edmonton":"#b2df8a",
      "Kansas":"#33a02c",
      "Seattle":"#fb9a99",
      "SF":"#e31a1c",
      "NYC":"#fdbf6f",
      "Boston":"#ff7f00",
      "Austin":"#cab2d6",
      "Raleigh":"#6a3d9a",
      "All Cities":"#ffff99"}
 
  #for key in m.keys():
  #  plt.plot(axis, m[key], marker=_marker[key], label=key)
  
  N = 3
  width = 0.07
  ind = np.arange(N)
  print ind
  fig, ax = plt.subplots()
  count = 1
  for key in s:
    rec0 = ax.bar(ind+count*width, m[key], width, color=_color[key])
    count += 1
  
  plt.ylim(0, 1.0)
#  plt.xlabel('Attribute Type', fontsize=25)
  plt.ylabel('Percentage of Datasets', fontsize=30)
  plt.xticks(ind+0.4, label, fontsize=25)
  plt.yticks(fontsize=17)
#  ax.legend(s,prop={'size':10.5},loc=1)

  plt.show()

if __name__=="__main__":
  main(sys.argv[1:])

