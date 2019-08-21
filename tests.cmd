REM Test w/ defaults
py csvToGeoJSON.py --verbose
REM Test w/ no ID column and different column names
REM CSV fields: Country,Capital City,Latitude,Longitude,lat,lon
py csvToGeoJSON.py --csv csv/country_cap_latlon.csv --output output/countr_cap_latlon.geoJSON --verbose --columns "{ 'latitude': 'lat', 'longitude': 'lon', 'name': 'Capital City', 'value': 'Country' }"
REM Test w/ no ID column and different column names and order
REM CSV fields: pointid,label,lat,long,name,GDP
py csvToGeoJSON.py --csv csv/alternative-columns-test.csv --output output/alternative-columns-test.geoJSON --verbose --columns "{ 'id':'-auto-', 'latitude': 'lat', 'longitude': 'long', 'name': 'label', 'value': 'GDP' }"
