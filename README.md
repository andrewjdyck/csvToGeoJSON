
## csvToGeoJSON converter ##

This python script takes data in csv format and converts to geoJSON format for use in mapping applications on the web.

Two sample CSV documents, sample.csv and country_cap_latlon.csv, are included that can be used to show how the utility works. 

By default, the script expects CSV data be in the format specified in the sample data 'sample.csv'. However, you can specify other formats in the program arguments. 

csvToGeoJSON arguments (all optional):

  -h, --help         Show this help message and exit
  --verbose, --v     Show parameters, detailed messages and geoJSON output
  --csv CSV          Filepath/name of CVS input file
                     Default: sample.csv
  --output OUTPUT    Filepath/name of GeoJSON output file
                     Default: output.geojson
  --columns COLUMNS  JSON-formatted dictionary that maps CSV column names to
                     GeoJSON fields.
                     Default: "{ 'id':'id', 'latitude':'lat', 'longitude':'lon', 'name':'name', 'value':'pop' }"
                     where each name:value pair is {geoJSON-column}:{CSV-column}
                     Note: CSV columns don't have to appear in a particular order since the position of the data columns will be determined from their order in the CSV header (first row).
                     If CSV contains no ID field, specifying 'id':'-auto-' will automatically generate an ID value based on the row # of the CSV. Otherwise, the ID value will be 0.

Questions and comments to info@andrewdyck.com