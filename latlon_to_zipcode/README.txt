- Download US Shapefile: ftp://ftp2.census.gov/geo/tiger/TIGER2013/ZCTA5/tl_2013_us_zcta510.zip
- Extract to ./shapefile/
- If point.txt and bbox.csv are not existed in converted_shapefile/
 + Run $./convert.sh to convert original shapefile to point.txt and bbox.csv
- Compile: run $make
- Run a test: 
  
 	$./zipcode 40.667098 -73.982363

- Run a full conversion: 

	$./zipcode 

 + Input: latlon.txt: each line in this file refers to a file that contain lat/lon. Each line of lat/lon file has the format: lat,lon 
