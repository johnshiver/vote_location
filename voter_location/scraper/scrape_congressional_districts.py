from bs4 import BeautifulSoup
import requests


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


ny_url = "https://en.wikipedia.org/wiki/New_York's_8th_congressional_district"
pa_url = "https://en.wikipedia.org/wiki/Pennsylvania's_6th_congressional_district"


ny_res = requests.get(ny_url)
ny_soup = BeautifulSoup(ny_res.content, "html.parser")

#pa_res = requests.get(pa_url)
#pa_soup = BeautifulSoup(pa_res.content, "html.parser")

for child in ny_soup.childGenerator():
    recursiveChildren(child)

if congress_photo:
    with open('{}.jpg'.format(congress_rep), 'wb') as f:
        photo_res = requests.get("https:{}".format(congress_photo))
        f.write(photo_res.content)
