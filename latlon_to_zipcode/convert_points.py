output = open("converted_shapefile/point.txt", "w")
output.write("33144\n")
with open("converted_shapefile/point.csv") as lines:
	for line in lines:
		a = line.strip("\n").split("\t")
		zipcode = a[0]
		output.write(a[0] + "\n" + "1" + "\n" + str(len(a) - 1) + "\n")
		for latlon in a[1:]:
			x = latlon.split(",")
			lon = x[0]
			lat = x[1]
			output.write(lon + " " + lat + "\n")
