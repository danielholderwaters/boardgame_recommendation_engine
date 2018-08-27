#this is a recommendation engine project using boardgamegeek's API.
#check this one out: https://apps.quanticfoundry.com/recommendations/tabletop/boardgame/
#here is the preferred boardgamegeek python API package https://github.com/lcosmin/boardgamegeek/blob/develop/boardgamegeek/main.py
import os
os.chdir('/mnt/c/Users/danie/Desktop/PythonCode')
print ("current working directory is:", os.getcwd())

#i dont know why, but after creating a virtual environment, this command prompt syntax works in linux:
#sudo python -m pip install boardgamegeek
import boardgamegeek
