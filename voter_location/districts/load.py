import os
from django.contrib.gis.utils import LayerMapping
from .models import District

district_mapping = {
    'statename' : 'STATENAME',
    'd_id' : 'ID',
    'district' : 'DISTRICT',
    'startcong' : 'STARTCONG',
    'endcong' : 'ENDCONG',
    'districtsi' : 'DISTRICTSI',
    'county' : 'COUNTY',
    'page' : 'PAGE',
    'law' : 'LAW',
    'note' : 'NOTE',
    'bestdec' : 'BESTDEC',
    'finalnote' : 'FINALNOTE',
    'rnote' : 'RNOTE',
    'lastchange' : 'LASTCHANGE',
    'fromcounty' : 'FROMCOUNTY',
    'geom' : 'MULTIPOLYGON',
}


district_shp = "/home/john/projects/voter_location/districtShapes/districts114.shp"

def run(verbose=True):
    lm = LayerMapping(
        District, district_shp, district_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=False, verbose=verbose)
