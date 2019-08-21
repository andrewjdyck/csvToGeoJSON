import csv
import argparse
import json

#### ========================================================================
#### csvToGeoJSON
####  - Tool to convert CSV file of geographic data into
####    JSON-formatted file of GeoJSON features                 
#### ========================================================================

class GeoFeature:
    ''' Object to hold properties of GeoJSON Feature '''
    def __init__(self):
        self.id = 0
        self.latitude = 0
        self.longitude = 0
        self.name = "-NA-"
        self.value = "-NA-"
    def print(self):
        print( "{ id = %s, latitude = %s, longitude = %s, name = %s, value = %s }" 
        % (self.id, self.latitude, self.longitude, self.name, self.value)
            )

class GeoFeatureColumn:
    ''' Object to hold mapping of GeoJSON fields to CSV field columns/indexes '''
    def __init__(self, geoJSONField, CSVName, CSVIndex ):
        self.geoJSONField = geoJSONField    # name of GeoJSON property
        self.CSVName = CSVName              # name of CSV column for this property
        self.CSVIndex = CSVIndex            # index of CSV column for this property

def main():

    # parse program arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '--v', action="store_true", help="Show parameters, detailed messages and geoJSON output")
    parser.add_argument('--csv', type=str, help="Filepath/name of CVS input file", default="sample.csv" )
    parser.add_argument('--output', type=str, help="Filepath/name of GeoJSON output file", default="output.geojson" )
    parser.add_argument('--columns',type=str, help="JSON-formatted dictionary that maps CSV column names to GeoJSON fields.", 
        default="{ 'id': 'id', 'latitude': 'lat', 'longitude': 'lon', 'name': 'name', 'value': 'pop' }")
    args = parser.parse_args()

    if args.verbose:
        print( "Arguments:" )
        print( "  Output = %s" % args.output )
        print( "  CSV = %s" % args.csv )
        print( "  Columns = %s" % args.columns )
        print()

    # parse "columns" argument into dictionary of CSV column names mapped to GeoJSON properties
    args.columns = args.columns.replace("'","\"")
    diCSVColumns = json.loads(args.columns)
    # print ("Columns = %s"  % json.dumps(diCSVColumns))

    # dictionary of all GeoFeatureColumns and their default mapping to CSV columns
    diGeoColumns = { 
        "id": GeoFeatureColumn("id","id",-1),
        "latitude": GeoFeatureColumn("latitude","lat",-1),
        "longitude": GeoFeatureColumn("longitude","long",-1),
        "name": GeoFeatureColumn("name","name",-1),
        "value": GeoFeatureColumn("value","value",-1)
    }

    # set the CSVNames of all diGeoColumns given in the "columns" argument
    if ( "id" in diCSVColumns ): diGeoColumns["id"].CSVName = diCSVColumns["id"]
    if ( "latitude" in diCSVColumns ): diGeoColumns["latitude"].CSVName = diCSVColumns["latitude"]
    if ( "longitude" in diCSVColumns ): diGeoColumns["longitude"].CSVName = diCSVColumns["longitude"]
    if ( "name" in diCSVColumns ): diGeoColumns["name"].CSVName = diCSVColumns["name"]
    if ( "value" in diCSVColumns ): diGeoColumns["value"].CSVName = diCSVColumns["value"]

    errors = [] # list of errors found, if any
    error = ""

    # Read in raw data from csv
    rawData = csv.reader(open(args.csv, 'r'), dialect='excel')

    # the template. where data from the csv will be formatted to geojson
    template = """
            {   "type" : "Feature",
                "id" : %s,
                "geometry" : {
                    "type" : "Point",
                    "coordinates" : ["%s","%s"]
                },
                "properties" : {
                    "name" : "%s", 
                    "value" : "%s" 
                }
            }"""

    # the head of the geojson file
    output = """{ "type" : "Feature Collection",
    { "features" : ["""

    # loop through the csv by row skipping the first
    iRow = 0
    for row in rawData:
        if iRow == 0: # If first row (CSV header)
            # determine column indexes of the values we need for GeoJSON
            iCol = 0
            if args.verbose: print( "CSV Columns:")
            
            for col in row:
                for fld in diGeoColumns:
                    # if CSV header column matches CSV field, remember this field's index
                    geoJSONField = ""
                    if col == diGeoColumns[fld].CSVName:
                        diGeoColumns[fld].CSVIndex = iCol
                        geoJSONField = " = geoJSON \"" + diGeoColumns[fld].geoJSONField + "\""
                        break
                if args.verbose: print( f'  column[{iCol}] = {quote(col):10}{geoJSONField}' )
                iCol+=1
            
            if args.verbose: print()

            # report geoJSON columns that are missing from CSV header as errors
            for fld in diGeoColumns:
                if diGeoColumns[fld].CSVIndex < 0: 
                    error = "No '%s' column in CSV header" % diGeoColumns[fld].geoJSONField
                    if diGeoColumns[fld].geoJSONField == "id" and diGeoColumns[fld].CSVName == "-auto-":
                        error += " (using row # since -auto- was specified)"
                    errors.append(error)

        else:  # if this is a data row
            # populate a GeoFeature from its corresponding columns in the data row
            featureRow = GeoFeature()

            # if CSV row contains GeoJSON column, set GeoFeature property to its value
            # otherwise, property's value is GeoFeature default

            # set GeoFeature.id from CSV column or from row # if set to "-auto-"
            if diGeoColumns["id"].CSVIndex >= 0: featureRow.id = row[diGeoColumns["id"].CSVIndex]
            elif diGeoColumns["id"].CSVName == "-auto-": featureRow.id = iRow
            # set GeoFeature.latitude from CSV column
            if diGeoColumns["latitude"].CSVIndex >= 0: featureRow.latitude = row[diGeoColumns["latitude"].CSVIndex]
            # set GeoFeature.longitude from CSV column
            if diGeoColumns["longitude"].CSVIndex >= 0: featureRow.longitude = row[diGeoColumns["longitude"].CSVIndex]
            # set GeoFeature.name from CSV column
            if diGeoColumns["name"].CSVIndex >= 0: featureRow.name = row[diGeoColumns["name"].CSVIndex]
            # set GeoFeature.value from CSV column
            if diGeoColumns["value"].CSVIndex >= 0: featureRow.value = row[diGeoColumns["value"].CSVIndex]
            
            # append comma between features (but not at end)
            if iRow > 1: output += ","

            # append formated GeoJSON Feature
            output += template % (
                    featureRow.id, 
                    featureRow.latitude, 
                    featureRow.longitude, 
                    featureRow.name,
                    featureRow.value
                )
        iRow += 1
            
    # the tail of the geojson file
    output += """
        ]
    }
}"""
    
    # print any errors that were found
    if len(errors):
        print("Errors:")
        for error in errors:
            print("  %s" % error)
        print()

    if args.verbose:
        print("GeoJSON Output:")
        print("=========================================================================")
        print(output)
        print("=========================================================================")
    
    # opens an geoJSON file to write the output to
    outFileHandle = open(args.output, "w")
    outFileHandle.write(output)
    outFileHandle.close()

# end main()

# Utility functions

def quote(s):
    ''' return string argument wrapped in double-quotes '''
    return "\"" + s + "\""

main()

    


    