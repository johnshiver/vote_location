from bs4 import BeautifulSoup
import requests

from django.core.management.base import BaseCommand, CommandError

from districts.models import DistrictDetail


congress_rep = ""
congress_photo = ""

def recursiveChildren(x):
    global congress_rep
    global congress_photo
    if congress_rep and not congress_photo and congress_rep in x.__str__():
        y = x.find_next('a', {'class': 'image'})
        c_name = "_".join(congress_rep.split())
        if y and c_name in y.img['src']:
            congress_photo = y.img['src']
    if "childGenerator" in dir(x):
        for child in x.childGenerator():
            name = getattr(child, "name", None)
            #if name is not None:
            #    pass
            recursiveChildren(child)
    else:
       if not x.isspace(): #Just to avoid printing "\n" parsed from document.
          if "Current\xa0Representative" in x.__str__():
              congress = x.find_next()
              congress = congress.find_next("a")
              congress_rep = congress.contents[0]


class Command(BaseCommand):

    def handle(self, *args, **options):
        global congress_rep
        global congress_photo
        all_districts = DistrictDetail.objects.all()
        for district in all_districts:
            res = requests.get(district.wikipedia_url)
            if 200 <= res.status_code < 300:
                soup = BeautifulSoup(res.content, "html.parser")
                for child in soup.childGenerator():
                   recursiveChildren(child)
                print(str(district) + " " + congress_rep + " " + congress_photo)
                if congress_rep:
                    district.politician_name = congress_rep
                if congress_photo:
                    if "75px" in congress_photo:
                        congress_photo = congress_photo.replace("75px", "150px")
                    congress_rep = "_".join(congress_rep.lower().split())
                    photo_dest = "/hdd_fast/congress_rep_photos/{}.jpg".format(congress_rep)
                    with open(photo_dest, 'wb') as f:
                        photo_rs = requests.get("https:{}".format(congress_photo))
                        if 200 <= photo_rs.status_code < 300:
                            f.write(photo_rs.content)
                            district.politician_image_url = photo_dest
                #district.save()
                congress_rep = ""
                congress_photo = ""
            else:
                print("error getting url {}".format(district.wikipedia_url))

