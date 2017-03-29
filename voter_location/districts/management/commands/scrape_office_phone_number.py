import re

from bs4 import BeautifulSoup
import requests

from django.core.management.base import BaseCommand, CommandError

from districts.models import DistrictDetail


class Command(BaseCommand):

    def handle(self, *args, **options):
        all_districts = DistrictDetail.objects.all()
        for district in all_districts:
            politician_name = district.politician_name
            if not politician_name:
                continue
            print("Finding {}".format(politician_name))
            # trying 2 urls because if there is a conflicting name
            # politician will use their full name
            url1 = "https://{}.house.gov".format(politician_name.split()[-1].lower())
            url2 = "https://{}.house.gov".format("".join(politician_name.split()).lower())
            if politician_in_page(url1, politician_name):
                phone_number = find_number_from_page(url1)
            elif politician_in_page(url2, politician_name):
                phone_number = find_number_from_page(url2)
            else:
                phone_number = ""

            if not phone_number:
                print("Couldnt find phone number for {}".format(politician_name))
            else:
                district.phone_number = phone_number
                district.save()
                print("{}: {}".format(district, phone_number))


def find_number_from_page(url):
    res = requests.get(url)
    phone_numbers = re.findall("(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4})", str(res.content))
    for number in phone_numbers:
        if "202" in number:
            return number
    else:
        return ""

def politician_in_page(url, politician_name):
    try:
        res = requests.get(url)
    except Exception as e:
        return False

    if not 200 <= res.status_code < 300:
        print("reqeust for {} failed".format(url))
        return False

    if politician_name in str(res.content):
        return True
    else:
        False

