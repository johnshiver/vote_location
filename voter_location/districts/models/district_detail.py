from django.db import models


class DistrictDetail(models.Model):

    district_shape = models.OneToOneField('districts.District')

    # politician info
    # politician = models.ForeignKey('politicians.Politician')
    # TODO: will eventually replace with its own model
    politician_name = models.CharField(max_length=100, default="")
    politician_party = models.CharField(max_length=20, default="")
    politician_image_url = models.CharField(max_length=100, default="")
    politician_url = models.CharField(max_length=200, default="")

    # district info
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
        if district_id == 0:
            district_id = 1
        state_name = "_".join(state_name.split())
        state_name += "'s"
        district_id = "{}{}".format(district_id,
                                    self._append_int(district_id))
        return base_url.format(state_name, district_id)

    @property
    def politician_ballotpedia_url(self):
        base_url = "https://ballotpedia.org/{}"
        fix_name = "_".join(self.politician_name.split())
        return base_url.format(fix_name)

    def get_politician_image_url(self):
        if self.politician_name:
            url = "_".join(self.politician_name.lower().split())
            return url + ".jpg"
        else:
            return ""

    def _append_int(self, num):
        if num > 9:
            secondToLastDigit = str(num)[-2]
            if secondToLastDigit == '1':
                return 'th'
        lastDigit = num % 10
        if lastDigit == 1:
            return 'st'
        elif lastDigit == 2:
            return 'nd'
        elif lastDigit == 3:
            return 'rd'
        else:
            return 'th'

