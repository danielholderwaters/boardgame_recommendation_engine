from pdb import set_trace
import os
import jsonpickle
import datetime
import sys
sys.path.append('C:/Users/danie/Desktop/PythonCode') # this line is necessary for calling the game module, which exists in the same directory as this file
from game import Game

#for my system, the following is the directory:
os.chdir('C:/Users/danie/Desktop/PythonCode')
print ("current working directory is:", os.getcwd())



INPUT_PATH = "BoardGameGeek.xml/%s/boardgame_batches/"
OUTPUT_PATH = "BoardGameGeek.json/%s/boardgame_batches/"

if len(sys.argv) > 1:
    DATE_DIR = sys.argv[1]
else:
    DATE_DIR = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m")

#ensure the prior scripts were run in the same month, or this won't work
input_dir = INPUT_PATH % DATE_DIR
output_dir = OUTPUT_PATH % DATE_DIR
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in sorted(os.listdir(input_dir)):
    output_filename = filename.replace(".xml", ".json")
    output_path = os.path.join(output_dir, output_filename)
    if os.path.exists(output_path):
        print "Skipping %s" % output_filename
    else:
        print "Writing %s" % output_path
        game = Game.from_xml(open(os.path.join(input_dir, filename)))
        open(output_path, "w").write(jsonpickle.encode(game))
