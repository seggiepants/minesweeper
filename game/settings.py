import os
import json

path = os.path.dirname(os.path.realpath(__file__))   
file_path = os.path.join(path, '../settings.json')     
f = open(file_path, 'rt')
settings = json.loads(f.read())
f.close()
