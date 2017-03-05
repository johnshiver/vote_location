from django.contrib.gis.gdal import DataSource


district_shape_file = "/home/john/projects/voter_location/districtShapes/districts114.shp"
ds = DataSource(district_shape_file)
