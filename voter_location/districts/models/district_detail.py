from django.db import models


class DistrictDetail(models.Model):

    district_shape = models.OneToOneField('districts.District')
#    politician = models.ForeignKey('politicians.Politician')

    # TODO: will eventually replace with its own model
    politician_name = models.CharField(max_length=100)
    state_name = models.CharField(max_length=100)
    district_full_name = models.CharField(max_length=100)
    current_population = models.IntegerField()
    registered_voters = models.IntegerField()

