from bs4 import BeautifulSoup
import requests

from django.core.management.base import BaseCommand, CommandError

from districts.models import DistrictDetail


class Command(BaseCommand):

    def handle(self, *args, **options):
        test_run = options['test_run']
        scraper = DistrictScraper()
        scraper.scrape(update=test_run)

    def add_arguments(self, parser):
        parser.add_argument("--test_run",
                            action='store_true',
                            dest='test_run',
                            default=False,
                            help="Wont update object if True")




class DistrictScraper(object):

    def __init__(self):
        self.congress_rep = ""
        self.congress_photo = ""

    def scrape(self, update=False):
        """
        Method that encapsulates all logic to scrape every congressional
        district in the database for congress leader name + photo
        and saves results to disk.
        """
        all_districts = DistrictDetail.objects.all()
        lost_reps, found_reps = 0, 0
        lost_photos, found_photos = 0, 0
        for district in all_districts:
            print("Search {}".format(district))
            res = requests.get(district.wikipedia_url)
            if 200 <= res.status_code < 300:
                soup = BeautifulSoup(res.content, "html.parser")
                for child in soup.childGenerator():
                    self.recursiveChildren(child)

                if self.congress_rep:
                    print("Found {}".format(self.congress_rep))
                    found_reps +=1
                else:
                    print("Couldnt find rep")
                    lost_reps += 1


                if self.congress_photo:
                    print("Found {}".format(self.congress_photo))
                    found_photos +=1
                else:
                    print("Couldnt find photo")
                    lost_reps += 1

                if self.congress_rep:
                    district.politician_name = self.congress_rep
                if self.congress_photo:
                    # if we have congress photo, download it, save to disk
                    # then save location to district db entry
                    if "75px" in self.congress_photo:
                        congress_photo = self.congress_photo.replace("75px", "150px")
                    else:
                        congress_photo = self.congress_photo

                    congress_rep = "_".join(self.congress_rep.lower().split())
                    photo_dest = "/hdd_fast/congress_rep_photos/{}.jpg".format(congress_rep)

                    with open(photo_dest, 'wb') as f:
                        photo_rs = requests.get("https:{}".format(congress_photo))
                        if 200 <= photo_rs.status_code < 300:
                            f.write(photo_rs.content)
                            district.politician_image_url = photo_dest
                        else:
                            print("Wasnt able to download photo! {}".format(congress_photo))

                if update:
                    district.save()
                self.congress_rep = ""
                self.congress_photo = ""
            else:
                print("error getting url {}".format(district.wikipedia_url))
        print("Found {} reps".format(found_reps))
        print("Missing {} reps".format(lost_reps))
        print("Found {} photos".format(found_photos))
        print("Missing {} photos".format(lost_photos))

    def recursiveChildren(self, node):
        """
        Recursively searches all children of node until congress rep + photo
        are found.
        """

        # DONT TOUCH THIS, ORDER MATTERS AND IT IS VERY BRITTLE

        # if we found rep name but dont have the photo yet
        # and the current node we have contains the name of the rep
        # this is a good place to look for a photo
        if self.congress_rep and not self.congress_photo and self.congress_rep in node.__str__():
            y = node.find_next('a', {'class': 'image'})
            c_name = "_".join(self.congress_rep.split())
            if y and c_name in y.img['src']:
                self.congress_photo = y.img['src']

        # TODO: add more conditions to find photo
        # Figure out how many are misssing

        # no idea what this condition means
        # basically just recurses on all children
        if "childGenerator" in dir(node):
            for child in node.childGenerator():
                self.recursiveChildren(child)

        # not sure what this condition does
        # but is what sets congress rep
        if not self.congress_rep and not node.isspace and "Current\xa0Representative" in node.__str__():
            congress = node.find_next()
            congress = congress.find_next("a")
            if congress.contents:
                self.congress_rep = congress.contents[0]
