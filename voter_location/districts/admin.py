from django.contrib import admin
from django.contrib.gis import admin as geo_admin


from .models import District, DistrictDetail


geo_admin.site.register(District, geo_admin.GeoModelAdmin)
admin.site.register(DistrictDetail)
