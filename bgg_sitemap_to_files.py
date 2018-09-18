#this is a recommendation engine project using boardgamegeek's API.
#check this one out: https://apps.quanticfoundry.com/recommendations/tabletop/boardgame/
#here is the preferred boardgamegeek python API package https://github.com/lcosmin/boardgamegeek/blob/develop/boardgamegeek/main.py
#!!!IF ANY FILES ARE SAVED WITH SIZE 0, DELETE THOSE FILES AND RERUN THIS CODE!!!
import os
os.chdir('C:/Users/danie/Desktop/PythonCode')
print ("current working directory is:", os.getcwd())

from bs4 import BeautifulSoup
from httplib2 import Http
#adding the following import lines
import sys
import datetime

http = Http()

if len(sys.argv) > 1:
    DATE_DIR = sys.argv[1]
else:
    DATE_DIR = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m") #adding the .datetime function between datetime and .strftime

DUMP_DIR = os.path.join("BoardGameGeek.xml", DATE_DIR)
SITEMAP_DIRECTORY = os.path.join(DUMP_DIR, "maps")
#following if statement creates the file BGG xml directory within the current working directory.
if not os.path.exists(SITEMAP_DIRECTORY):
    os.makedirs(SITEMAP_DIRECTORY)

def req(*args, **kwargs):
    try:
        response, body = http.request(*args, **kwargs)
    except Exception as e: #changing the syntax on this line
        print ("Could not request %r %r: %s" % (args, kwargs, e)) #surrounding the print statement in parentheses
        return None, None
    return response, body

response, body = req('http://boardgamegeek.com/sitemapindex')
print(response)
print(body)
import time

soup = BeautifulSoup(body, "lxml")
quest = soup.find_all("loc")
print(type(quest))

for loc in soup.find_all("loc"):
    url = loc.string.strip()
    filename = url[url.rindex("sitemap_")+len("sitemap_"):]
    path = os.path.join(SITEMAP_DIRECTORY, filename)
    if os.path.exists(path):
        continue
    print ("%s -> %s" % (url, path)) #added parenthases to the print command
    response, body = req(url)
    open(path, "w").write(str(body)) #some of the pages were throwing back errors because they were "bytes" and not "str", adding the str() command ensures th
    time.sleep(.1) #reduced this to .1 because...I wanted the program to run faster
