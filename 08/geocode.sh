curl -F addressFile=@short.csv \
     -F vintage=Current_Current \
     -F benchmark=Public_AR_Current \
     -F layers=9 \
     "https://geocoding.geo.census.gov/geocoder/geographies/addressbatch"
