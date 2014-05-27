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


import shpUtils
import matplotlib.pyplot as plt


def loadZipcode(zipcodefile):
	m = {}
	with open(zipcodefile) as lines:
		for line in lines:
			a = line.strip("\n").split("\t")
			zipcode = a[0]
			occurencyNumb = int(a[1])
			m[zipcode] = occurencyNumb
	return m

#Declare inputs
zipcodefile = "nyc.csv"
shapefile = "shapefile/nyc_zipcta.shp"
#define colours
#colours = {0:"#F7FCF0", 1:"#E0F3DB", 2:"#CCEBC5", 3:"#A8DDB5", 4:"#7BCCC4", 5:"#4EB3D3", 6:"#2B8CBE", 7:"#0868AC", 8:"#084081"}
colours = {0:"#ffffff", 1:"#fcfcff", 2:"#ebecff", 3:"#ebecff", 4:"#dadcff", 5:"#c9ccff", 6:"#b8bcff", 7:"#a7acff", 8:"#969cff", 9:"#858cff", 10:"#747cff", 11:"#636cff", 12:"#525dff", 13:"#414dff", 14:"#303dff", 15:"#1f2dff", 16:"#0e1dff", 17:"#0010fc", 18:"#000feb", 19:"#000eda", 20:"#000dc9", 21:"#000bb8", 22:"#000aa7"}
#colours = {0:"#F7FCF0", 1:"#F7FCF0", 2:"#E0F3DB", 3:"#E0F3DB", 4:"#CCEBC5", 5:"#CCEBC5", 6:"#A8DDB5", 7:"#7BCCC4", 8:"#4EB3D3", 9:"#2B8CBE", 10:"#0868AC", 11:"#084081"}
#colours = {0:"", 1:"", 2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:""}
#colours = {0:"#FFF7EC", 1:"#FEE8C8", 2:"#FDD49E", 3:"#FDBB84", 4:"#FC8D59", 5:"#EF6548", 6:"#D7301F", 7:"#B30000", 8:"#7F0000"}

# load the shapefile
shpRecords = shpUtils.loadShapefile(shapefile)
# load zipcodefile
m = loadZipcode(zipcodefile)
max = 0
min = 1000
for i in range(0,len(shpRecords)):
	zipcode =  shpRecords[i]["dbf_data"]["ZCTA5CE00"]
	if m[zipcode] > max:
		max = m[zipcode]
	if m[zipcode] < min:
		min = m[zipcode]
unit = (max-min)/22
print max
print min
for key in m.keys():
	m[key] = m[key] - min

for i in range(0,len(shpRecords)):
	# x and y are empty lists to be populated with the coordinates of each geometry.
	x = []
	y = []
	for j in range(0,len(shpRecords[i]['shp_data']['parts'][0]['points'])):
	# This is the number of vertices in the ith geometry.
	# The parts list is [0] as it is singlepart.
		# get x and y coordinates.
		tempx = float(shpRecords[i]['shp_data']['parts'][0]['points'][j]['x'])
		tempy = float(shpRecords[i]['shp_data']['parts'][0]['points'][j]['y'])
		x.append(tempx)
		y.append(tempy) # Populate the lists  

		# Creates a polygon in matplotlib for each geometry in the shapefile
	zipcode = shpRecords[i]["dbf_data"]["ZCTA5CE00"]
	if m.has_key(zipcode):
		colour = colours[m[zipcode]/unit]
	else:
		colour = colours[0]
	plt.fill(x, y, fc=colour, ec='0.7', lw=0.1)

#Create legend
p0 = plt.Rectangle((0, 0), 1, 1, fc=colours[0])
p1 = plt.Rectangle((0, 0), 1, 1, fc=colours[2])
p2 = plt.Rectangle((0, 0), 1, 1, fc=colours[4])
p3 = plt.Rectangle((0, 0), 1, 1, fc=colours[6])
p4 = plt.Rectangle((0, 0), 1, 1, fc=colours[8])
p5 = plt.Rectangle((0, 0), 1, 1, fc=colours[10])
p6 = plt.Rectangle((0, 0), 1, 1, fc=colours[12])
p7 = plt.Rectangle((0, 0), 1, 1, fc=colours[14])
p8 = plt.Rectangle((0, 0), 1, 1, fc=colours[16])
p9 = plt.Rectangle((0, 0), 1, 1, fc=colours[18])
p10 = plt.Rectangle((0, 0), 1, 1, fc=colours[20])
p11 = plt.Rectangle((0, 0), 1, 1, fc=colours[22])
extra = plt.Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
#This legend will show the exact number
plt.legend([p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11],\
["0-%d records" %((2*unit-1)),\
"%d-%d records" %(2*unit,(4*unit-1)),\
"%d-%d records" %(4*unit,(6*unit-1)),\
"%d-%d records" %(6*unit,(8*unit-1)),\
"%d-%d records" %(8*unit,(10*unit-1)),\
"%d-%d records" %(10*unit,(12*unit-1)),\
"%d-%d records" %(12*unit,(14*unit-1)),\
"%d-%d records" %(14*unit,(16*unit-1)),\
"%d-%d records" %(16*unit,(18*unit-1)),\
"%d-%d records" %(18*unit,(20*unit-1)),\
"%d-%d records" %(20*unit,(22*unit-1)),\
">%d records" %(22*unit)],\
prop={'size':8}, loc = 2)

#The short version of legend:
plt.legend([extra, p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11],\
["Number of records",\
"0-%dk" %((2*unit/1000-1)),\
"%dk-%dk" %(2*unit/1000,(4*unit/1000-1)),\
"%dk-%dk" %(4*unit/1000,(6*unit/1000-1)),\
"%dk-%dk" %(6*unit/1000,(8*unit/1000-1)),\
"%dk-%dk" %(8*unit/1000,(10*unit/1000-1)),\
"%dk-%dk" %(10*unit/1000,(12*unit/1000-1)),\
"%dk-%dk" %(12*unit/1000,(14*unit/1000-1)),\
"%dk-%dk" %(14*unit/1000,(16*unit/1000-1)),\
"%dk-%dk" %(16*unit/1000,(18*unit/1000-1)),\
"%dk-%dk" %(18*unit/1000,(20*unit/1000-1)),\
"%dk-%dk" %(20*unit/1000,(22*unit/1000-1)),\
">%dk" %(22*unit/1000)],\
prop={'size':10.6}, loc = 2)

#plt.title("NYC ZipCode Overlap")
plt.axis('off')
plt.savefig('nycallzipcodeoverlap.jpg', format='jpg', dpi=700)
plt.show()
  
