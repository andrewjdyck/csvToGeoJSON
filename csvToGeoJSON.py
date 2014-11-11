import csv

# Read in raw data from csv
rawData = csv.reader(open('sample.csv', 'rb'), dialect='excel')

# the template. where data from the csv will be formatted to geojson
template = \
    ''' \
    { "type" : "Feature",
        "id" : %s,
            "geometry" : {
                "type" : "Point",
                "coordinates" : ["%s","%s"]},
        "properties" : { "name" : "%s", "value" : "%s"}
        },
    '''

# the head of the geojson file
output = \
    ''' \
{ "type" : "Feature Collection",
    {"features" : [
    '''

# loop through the csv by row skipping the first
iter = 0
for row in rawData:
    iter += 1
    if iter >= 2:
        id = row[0]
        lat = row[1]
        lon = row[2]
        name = row[3]
        pop = row[4]
        output += template % (row[0], row[1], row[2], row[3], row[4])
        
# the tail of the geojson file
output += \
    ''' \
    ]
}
    '''
    
# opens an geoJSON file to write the output to
outFileHandle = open("output.geojson", "w")
outFileHandle.write(output)
outFileHandle.close()

    


    