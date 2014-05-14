import sys
sys.path.append('../')
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
zipcodefile = "chicago.csv"
shapefile = "ZipCodes.shp"
#define colours
colours = {0:"#F7FCF0", 1:"#E0F3DB", 2:"#CCEBC5", 3:"#A8DDB5", 4:"#7BCCC4", 5:"#4EB3D3", 6:"#2B8CBE", 7:"#0868AC", 8:"#084081"}
colours = {0:"#ffffff", 1:"#fcfcff", 2:"#ebecff", 3:"#ebecff", 4:"#dadcff", 5:"#c9ccff", 6:"#b8bcff", 7:"#a7acff", 8:"#969cff", 9:"#858cff", 10:"#747cff", 11:"#636cff", 12:"#525dff", 13:"#414dff", 14:"#303dff", 15:"#1f2dff", 16:"#0e1dff", 17:"#0010fc", 18:"#000feb", 19:"#000eda", 20:"#000dc9", 21:"#000bb8", 22:"#000aa7"}
colours = {0:"#ffffff", 1:"#ebecff", 2:"#dadcff", 3:"#a7acff", 4:"#a7acff", 5:"#414dff", 6:"#0e1dff", 7:"#000eda", 8:"#000aa7"}
#colours = {0:"#F7FCF0", 1:"#F7FCF0", 2:"#E0F3DB", 3:"#E0F3DB", 4:"#CCEBC5", 5:"#CCEBC5", 6:"#A8DDB5", 7:"#7BCCC4", 8:"#4EB3D3", 9:"#2B8CBE", 10:"#0868AC", 11:"#084081"}
#colours = {0:"", 1:"", 2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:""}
#colours = {0:"#FFF7EC", 1:"#FEE8C8", 2:"#FDD49E", 3:"#FDBB84", 4:"#FC8D59", 5:"#EF6548", 6:"#D7301F", 7:"#B30000", 8:"#7F0000"}

# load the shapefile
shpRecords = shpUtils.loadShapefile(shapefile)
# load zipcodefile
m = loadZipcode(zipcodefile)
max = 0
for i in range(0,len(shpRecords)):
	zipcode =  shpRecords[i]["dbf_data"]["ZIP"]
	if m[zipcode] > max:
		max = m[zipcode]
unit = max/8
print max

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
	zipcode = shpRecords[i]["dbf_data"]["ZIP"]
	if m.has_key(zipcode):
		colour = colours[m[zipcode]/unit]
	else:
		colour = colours[0]
	plt.fill(x, y, fc=colour, ec='0.7', lw=0.1)

#Create legend
p0 = plt.Rectangle((0, 0), 1, 1, fc=colours[0])
p1 = plt.Rectangle((0, 0), 1, 1, fc=colours[1])
p2 = plt.Rectangle((0, 0), 1, 1, fc=colours[2])
p3 = plt.Rectangle((0, 0), 1, 1, fc=colours[3])
p4 = plt.Rectangle((0, 0), 1, 1, fc=colours[4])
p5 = plt.Rectangle((0, 0), 1, 1, fc=colours[5])
p6 = plt.Rectangle((0, 0), 1, 1, fc=colours[6])
p7 = plt.Rectangle((0, 0), 1, 1, fc=colours[7])
p8 = plt.Rectangle((0, 0), 1, 1, fc=colours[8])
extra = plt.Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)

plt.legend([extra, p0,p1,p2,p3,p4,p5,p6,p7,p8],\
["Number of records",\
"0-%d records" %((1*unit-1)),\
"%d-%d records" %(1*unit,(2*unit-1)),\
"%d-%d records" %(2*unit,(3*unit-1)),\
"%d-%d records" %(3*unit,(4*unit-1)),\
"%d-%d records" %(4*unit,(5*unit-1)),\
"%d-%d records" %(5*unit,(6*unit-1)),\
"%d-%d records" %(6*unit,(7*unit-1)),\
"%d-%d records" %(7*unit,(8*unit-1)),\
">%d records" %(8*unit)],\
prop={'size':10}, loc = 1)

plt.legend([extra, p0,p1,p2,p3,p4,p5,p6,p7,p8],\
["Number of records",\
"0-%dk" %((1*unit/1000-1)),\
"%dk-%dk" %(1*unit/1000,(2*unit/1000-1)),\
"%dk-%dk" %(2*unit/1000,(3*unit/1000-1)),\
"%dk-%dk" %(3*unit/1000,(4*unit/1000-1)),\
"%dk-%dk" %(4*unit/1000,(5*unit/1000-1)),\
"%dk-%dk" %(5*unit/1000,(6*unit/1000-1)),\
"%dk-%dk" %(6*unit/1000,(7*unit/1000-1)),\
"%dk-%dk" %(7*unit/1000,(8*unit/1000-1)),\
">%dk" %(8*unit/1000)],\
prop={'size':10.6}, loc = 3)

#plt.title("Chicago ZipCode Overlap")
plt.axis('off')
plt.savefig('chicagoallzipcode.jpg', format='jpg', dpi=700)
plt.show()
  
