from django.contrib.gis.db import models


class District(models.Model):
    """
    This model maps directly to shape file, note this uses
    gis.db and not the regular django db library.
    """
    statename = models.CharField(max_length=50)
    d_id = models.CharField(max_length=12)
    district = models.CharField(max_length=2)
    startcong = models.CharField(max_length=10)
    endcong = models.CharField(max_length=10)
    districtsi = models.CharField(max_length=32)
    county = models.CharField(max_length=32)
    page = models.CharField(max_length=32)
    law = models.CharField(max_length=32)
    note = models.CharField(max_length=32)
    bestdec = models.CharField(max_length=32)
    finalnote = models.CharField(max_length=26)
    rnote = models.CharField(max_length=32)
    lastchange = models.CharField(max_length=29)
    fromcounty = models.CharField(max_length=2)
    geom = models.MultiPolygonField(srid=4269)

    def __str__(self):
        return "{}: {}".format(self.statename, self.district)

