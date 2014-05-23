- download
  Download datasets in JSON format.

- schema_similarity
  Compute the similarity between schemata.

- matrix_heatmap
  Generate matrix heatmap using schema similarity scores.

- metadata
  Retrieve metadata including tags, schema, description using Socrata APIs

- tagcloud (Require result from metadata)
  Generate tag cloud using tags associated with the dataset.

- type_detection
  Detect attribute type

- barchart (Require result from type_detection)
  Generate a barchart of data type ratio across cities.  

- extract_zipcode_latlon (Require result from type_detection)
  Read result from type_detection and extract all lat/lon, zipcode values .

- latlon_to_zipcode
  Convert lat/long to zipcode.

- heatmap (Require result from extract_zipcode_latlon and latlon_to_zipcode)
  Generate a heat map of geographical coverage based on zip code values in NYC
and Chicago.

