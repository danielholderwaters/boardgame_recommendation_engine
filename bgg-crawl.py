from httplib2 import Http
import os
import re
import datetime #this module needs to be imported along with the original time module
import sys
import time

os.chdir('C:/Users/danie/Desktop/PythonCode')
print ("current working directory is:", os.getcwd())

#DATE_DIR is a 6 character string with the %Y%m format. september 2018 will be "201809"
if len(sys.argv) > 1:
    DATE_DIR = sys.argv[1]
else:
    DATE_DIR = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m")

#DUMP_DIR is a folder in your working directory ending with \BoardGameGeek.xml\DATE_DIR
DUMP_DIR = os.path.join("BoardGameGeek.xml", DATE_DIR)
#SITEMAP_DIRECTORY is the name of a sub-folder of DUMP_DIR called "maps"
SITEMAP_DIRECTORY = os.path.join(DUMP_DIR, "maps")
#GAME_OUTPUT_DIRECTORY is the name of a sub-folder of maps called "boardgame_batches"
GAME_OUTPUT_DIRECTORY = os.path.join(DUMP_DIR, "boardgame_batches")
#GEETKLIST_OUTPUT_DIRECTORY is the name of a sub-folder of maps called "geeklist"
GEEKLIST_OUTPUT_DIRECTORY = os.path.join(DUMP_DIR, "geeklist")
#GAME_NUMBER is a string compiled of the subfolder 'boardgame' and ending with a game number. this will be the game's file
GAME_NUMBER = re.compile("/boardgame/([0-9]+)/")
#GEEKLIST_NUMBER is similar to GAME_NUMBER but with a 'geeklist' sub-folder
GEEKLIST_NUMBER = re.compile("/geeklist/([0-9]*)/")

#this for loop creates subfolders if they don't already exist
for d in GAME_OUTPUT_DIRECTORY, GEEKLIST_OUTPUT_DIRECTORY:
    if not os.path.exists(d):
        os.makedirs(d)

BATCH_SIZE = 20

#these are the base urls for scraping.  notice the %s formatting.  this is where the boardgame or geeklist number will go
BOARDGAME_URL = "http://boardgamegeek.com/xmlapi/boardgame/%s?comments=1&stats=1"
GEEKLIST_URL = "http://boardgamegeek.com/xmlapi/geeklist/%s?comments=1"

http = Http()

def req(*args, **kwargs):
    try:
        response, body = http.request(*args, **kwargs)
    except Exception as e: #changing syntax here
        print ("Could not request %r %r: %s" % (args, kwargs, e)) #changing syntax here
        return None, None
    return response, body

def download_geeklist(number):
    filename = os.path.join(GEEKLIST_OUTPUT_DIRECTORY, "geeklist-%s.xml" % number)
    if os.path.exists(filename):
        print ("Skipping %s" % filename) #changing syntax here for python3
        return False
    url = GEEKLIST_URL % number
    if number in ("36742", "35076", "34435", "30058", "29485", "16221", "8785", "4368", "49088"):
        # For whatever reason these are known to be bad.
        return False
    print ("Downloading geeklist %s" % number)
    response, body = req(
        url, "GET", headers = {
            "Accept-Encoding": "gzip,deflate",
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0)" })
    if body is not None:
        open(filename, "wb").write(body)
    return True

#defining the function to download a single boardgame's webpage as xml format
def download_boardgame_batch(numbers):
    url = BOARDGAME_URL % ",".join(numbers)
    if len(numbers) == 1:
        filename = "boardgame-" + numbers[0] + ".xml"
    else:
        filename = "boardgame-" + numbers[0] + "-" + numbers[-1] + ".xml"
    path = os.path.join(GAME_OUTPUT_DIRECTORY, filename)
    if os.path.exists(path):
        print ("Skipping %s, already present." % path)
        return False
    print (filename, url)
    response, body = req(url, "GET", headers={
            "Accept-Encoding": "gzip,deflate",
            "User-Agent": "Mozilla/5.0 (X11; U; Linux i586; de; rv:5.0) Gecko/20100101 Firefox/5.0" })
    if body is not None:
        open(path, "wb").write(body)
    return True

def crawl_boardgame_file(filename):
    """Download the listing for every board game in a single site map file."""
    print ("Processing %s" % filename)
    numbers = []
    for line in open(filename):
        match = GAME_NUMBER.search(line)
        if match is not None:
            (number,) = match.groups()
            numbers.append(number)
            if len(numbers) >= BATCH_SIZE:
                try:
                    made_request = download_boardgame_batch(numbers)
                except  Exception as e:
                    made_request = download_boardgame_batch(numbers)
                if made_request:
                    time.sleep(1)
                numbers = []
    # Do one last batch.
    if len(numbers) > 0:
        download_boardgame_batch(numbers)

def crawl_geeklist_file(filename):
    numbers = []
    for line in open(filename):
        match = GEEKLIST_NUMBER.search(line)
        if match is not None:
            number = match.groups()[0]
            made_request = download_geeklist(number)
            if made_request:
                time.sleep(0.5)

def crawl_boardgames():
    """Download the listing for every board game in the site map."""
    for filename in os.listdir(SITEMAP_DIRECTORY):
        if '_boardgame_' in filename:
            print("printing:", filename)
            crawl_boardgame_file(os.path.join(SITEMAP_DIRECTORY, filename))

def crawl_geeklists():
    for filename in os.listdir(SITEMAP_DIRECTORY):
        if 'geeklist' in filename:
            crawl_geeklist_file(os.path.join(SITEMAP_DIRECTORY, filename))

crawl_boardgames()
#crawl_geeklists()
