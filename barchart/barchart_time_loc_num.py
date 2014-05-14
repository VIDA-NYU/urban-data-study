import sys
import matplotlib.pyplot as plt
import numpy as np

def getData():
  with open("time_loc_number.csv") as lines:
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
  label = ["Time", "Location", "Number", "Null"] #Label for x axis
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
  
  N = 4
  width = 0.07
  ind = np.arange(N)
  print ind
  fig, ax = plt.subplots()
  count = 1
  for key in s:
    rec0 = ax.bar(ind+count*width, m[key], width, color=_color[key])
    count += 1
  plt.ylim(0,1.0)

  plt.ylabel('Percentage of Datasets', fontsize=30)
  plt.xticks(ind+0.5, label, fontsize=25)
  plt.tick_params(axis='y', labelsize=17)
  ax.legend(s, loc=1,prop={'size':13})

  plt.show()

if __name__=="__main__":
  main(sys.argv[1:])

