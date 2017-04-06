import os.path
from pprint import pprint

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
                            default=True,
                            help="Wont update object if True")


class DistrictScraper(object):

    found_photo_logs = "found_photo_logs"
    lost_photo_logs = "lost_photo_logs"
    found_rep_logs = "found_rep_logs"
    lost_rep_logs = "lost_rep_logs"

    def __init__(self):
        self.congress_rep = ""
        self.congress_photo = ""
        self.found_photos = []
        self.found_reps = []
        self.lost_photos = []
        self.lost_reps = []

    def scrape(self, update=False):
        """
        Method that encapsulates all logic to scrape every congressional
        district in the database for congress leader name + photo
        and saves results to disk.
        """
        # just incase
        self._clean_up()

        all_districts = DistrictDetail.objects.all()
#        all_districts = DistrictDetail.objects.filter(politician_name__contains="Nydia Velázquez")
        for district in all_districts:
            self.district = district
            res = requests.get(district.wikipedia_url)
            if 200 <= res.status_code < 300:
                soup = BeautifulSoup(res.content, "html.parser")
                for child in soup.childGenerator():
                    self.recursiveChildren(child)

                if self.congress_rep:
                    self.found_reps.append(self.congress_rep)
                else:
                    self.lost_reps.append(str(district))

                if not self.congress_photo:
                    if self.congress_rep:
                        self.lost_photos.append(self.congress_rep)
                    else:
                        self.lost_photos.append(str(district))

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
                    if update and not os.path.isfile(photo_dest):
                        with open(photo_dest, 'wb') as f:
                            photo_rs = requests.get("https:{}".format(congress_photo))
                            if 200 <= photo_rs.status_code < 300:
                                self.found_photos.append(congress_photo)
                                district.politician_image_url = photo_dest
                                print("adding {}".format(photo_dest))
                                f.write(photo_rs.content)
                            else:
                                district.politician_image_url = ""
                                self.lost_photos.append(congress_photo)
                if update:
                    district.save()
                self.congress_rep = ""
                self.congress_photo = ""
            else:
                print("error getting url {}".format(district.wikipedia_url))

        self.record_and_print_results()
        self._clean_up()

    def record_and_print_results(self):
        if os.path.isfile(self.found_rep_logs) and os.path.isfile(self.lost_rep_logs):
            self.compare_new_and_old(kind="reps")
        else:
            self.write_to_disk(kind="reps")
            print("Found reps: ")
            self.print_log(self.found_rep_logs)
            print("\n")
            print("#" * 45)
            print("Lost reps: ")
            self.print_log(self.lost_rep_logs)
            print("\n")
            print("#" * 45)

        if os.path.isfile(self.found_photo_logs) and os.path.isfile(self.lost_photo_logs):
            self.compare_new_and_old(kind="photos")
        else:
            self.write_to_disk(kind="photos")
            print("Found photos: ")
            self.print_log(self.found_photo_logs)
            print("\n")
            print("#" * 45)
            print("Lost photos: ")
            self.print_log(self.lost_photo_logs)
            print("\n")
            print("#" * 45)

    def compare_new_and_old(self, kind="reps"):
        if kind not in {"reps", "photos"}:
            raise ValueError("Arg error: kind must be reps or photos")

        if kind == "reps":
            old_found_reps = self.read_file(self.found_rep_logs)
            old_lost_reps = self.read_file(self.lost_rep_logs)
            new_found_reps = self.found_reps[:]
            new_lost_reps = self.lost_reps[:]
            new_found = set(new_found_reps) - set(old_found_reps)
            found_now_lost = set(old_found_reps) - set(new_found_reps)
            print("New reps found")
            pprint(new_found)
            print("\n")
            print("#" * 45)
            print("Reps we had but lost")
            pprint(found_now_lost)
            print("\n")
            print("#" * 45)
            print("remaining reps to find")
            pprint(new_lost_reps)
            print("\n")
            print("#" * 45)
            os.remove(self.found_rep_logs)
            os.remove(self.lost_rep_logs)
            self.write_to_disk(kind="reps")
        else:
            old_found_photos = self.read_file(self.found_photo_logs)
            old_lost_photos = self.read_file(self.lost_photo_logs)
            new_found_photos = self.found_photos[:]
            new_lost_photos = self.lost_photos[:]
            new_found = set(new_found_photos) - set(old_found_photos)
            found_now_lost = set(old_found_photos) - set(new_found_photos)
            print("New photos found")
            pprint(new_found)
            print("\n")
            print("#" * 45)
            print("Photos we had but lost")
            pprint(found_now_lost)
            print("\n")
            print("#" * 45)
            print("remaining photos to find")
            pprint(new_lost_photos)
            print("\n")
            print("#" * 45)
            os.remove(self.found_photo_logs)
            os.remove(self.lost_photo_logs)
            self.write_to_disk(kind="photos")

    def read_file(seff, file_name):
        logs = []
        with open(file_name, 'r') as f:
            for l in f.readlines():
                l = l.rstrip()
                logs.append(l)
        return logs

    def write_to_disk(self, kind="reps"):
        if kind not in {"reps", "photos"}:
            raise ValueError("Arg error: kind must be reps or photos")
        if kind == "reps":
            with open(self.found_rep_logs, 'w') as f:
                f.writelines([i + "\n" for i in self.found_reps])
            with open(self.lost_rep_logs, 'w') as f:
                f.writelines([i + "\n" for i in self.lost_reps])
        else:
            with open(self.found_photo_logs, 'w') as f:
                f.writelines([i + "\n" for i in self.found_photos])
            with open(self.lost_photo_logs, 'w') as f:
                f.writelines([i + "\n" for i in self.lost_photos])

    def print_log(self, file_name):
        logs = self.read_file(file_name)
        pprint(logs)

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
            d_name = "".join(self.congress_rep.split())
#            import ipdb;ipdb.set_trace()
            if y and c_name.lower() in str(y.img['src']).lower():
                self.congress_photo = y.img['src']
            elif y and d_name.lower() in str(y.img['src']).lower():
                self.congress_photo = y.img['src']
            elif y and self.district.politician_last_name.lower() in str(y.img['src']).lower():
                self.congress_photo = y.img['src']
            elif y and self.district.politician_first_name.lower() in str(y.img['src']).lower():
                self.congress_photo = y.img['src']
            elif y and self.district.politician_manual_photo_abrv:
                if self.district.politician_manual_photo_abrv.lower() in str(y.img['src']).lower():
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

    def _clean_up(self):
        self.found_reps = []
        self.found_photos = []
        self.lost_reps = []
        self.lost_photos = []
