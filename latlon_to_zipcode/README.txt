- Download US Shapefile: ftp://ftp2.census.gov/geo/tiger/TIGER2013/ZCTA5/tl_2013_us_zcta510.zip
- Extract to ./shapefile/
- If point.txt and bbox.csv are not existed in converted_shapefile/
 + Run $./convert.sh to convert original shapefile to point.txt and bbox.csv
- Compile: run $make
- Run a test: $./zipcode 40.667098 -73.982363
Or Convert all: $./zipcode (This mode will convert all lat/long in files listed in latlon.txt)
