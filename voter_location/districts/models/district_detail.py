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

    @property
    def wikipedia_url(self):
        base_url = "https://en.wikipedia.org/wiki/{}_{}_congressional_district"
        state_name = self.district_shape.statename
        district_id = int(self.district_shape.district)
        state_name = "_".join(state_name.split())
        state_name += "'s"
        #import ipdb;ipdb.set_trace()
        district_id = "{}{}".format(district_id,
                                    self._append_int(district_id))
        return base_url.format(state_name, district_id)

    def _append_int(self, num):
        if num > 9:
            secondToLastDigit = str(num)[-2]
            if secondToLastDigit == '1':
                return 'th'
        lastDigit = num % 10
        if (lastDigit == 1):
            return 'st'
        elif (lastDigit == 2):
            return 'nd'
        elif (lastDigit == 3):
            return 'rd'
        else:
            return 'th'

