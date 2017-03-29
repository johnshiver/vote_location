import requests

from django.core.management.base import BaseCommand, CommandError

from districts.models import DistrictDetail


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        all_districts = DistrictDetail.objects.all()
        for district in all_districts:
            r1 = requests.get(district.district_ballotpedia_url)
            r2 = requests.get(district.politician_ballotpedia_url)
            if not 200 <= r1.status_code < 300:
                print(district.district_ballotpedia_url)
            if not 200 <= r2.status_code < 300:
                print(district.politician_ballotpedia_url)

