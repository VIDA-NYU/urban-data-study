Open Data Analysis
=================
Please read README.txt in each directory to find the instruction to run the source code.
Below is the brief description of each directory: 
## download
 * Download datasets in JSON format. (Shell script)

## schema_similarity
 * Compute the similarity between schemata. (Python)

## matrix_heatmap
 * (Figure 8) Generate matrix heatmap using schema similarity scores. (Java Script)

## metadata
 * Retrieve metadata including tags, schema, description using Socrata APIs. (Python)

## tagcloud (
 * (Figure 5) Generate tag cloud using tags associated with the dataset. (R)
 * Require result from metadata

## type_detection
 * Detect attribute type (Python)

## barchart (Require result from type_detection)
 * (Figure 9) Generate a barchart of data type ratio across cities. (Python)

## extract_zipcode_latlon 
 * Read result from type_detection and extract all lat/lon, zipcode values. (Python)
 * Require result from type_detection

## latlon_to_zipcode
 * Convert lat/long to zipcode. (C++)

## heatmap 
 * (Figure 12) Generate a heat map of geographical coverage based on zip code values in NYC and Chicago. (Python)
 * Require result from extract_zipcode_latlon and latlon_to_zipcode
