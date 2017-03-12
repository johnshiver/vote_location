from django.db import models


class DistrictDetail(models.Model):

    district_shape = models.OneToOneField('districts.District')
#    politician = models.ForeignKey('politicians.Politician')

    # TODO: will eventually replace with its own model
    politician_name = models.CharField(max_length=100, default="")
    politician_party = models.CharField(max_length=20, default="")
    politician_image_url = models.CharField(max_length=100, default="")
    state_name = models.CharField(max_length=100)
    district_full_name = models.CharField(max_length=100)
    current_population = models.IntegerField()
    registered_voters = models.IntegerField()

    def __str__(self):
        return self.district_shape.statename + " " + self.district_shape.district

