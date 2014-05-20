import shapefile

sf = shapefile.Reader("shapefile/tl_2013_us_zcta510.shp")
bboxes = open("converted_shapefile/bboxes.csv", "w")
points = open("converted_shapefile/points.csv", "w")
shapes = sf.shapes()
records = sf.records()
# Read the bounding box from the 4th shape
for i in range(len(shapes)):
	bbox = str(records[i][0]) + "\t" + \
		str(shapes[i].bbox[0]) + "\t" + \
		str(shapes[i].bbox[1]) + "\t" + \
		str(shapes[i].bbox[2]) + "\t" + \
		str(shapes[i].bbox[3]) + "\n"
	bboxes.write(bbox)

	point = str(records[i][0])
	for p in shapes[i].points:
		point += "\t" + str(p[0]) + "," + str(p[1])
	points.write(point + "\n")

bboxes.close()
points.close()

