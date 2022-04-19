
# Placed this file to make this directory a package



import json
import os

# set version
try:
    with open( os.path.join( os.path.dirname(os.path.realpath(__file__)), "version.json"), "r") as fh:
        __version__ = json.load(fh)['version']
except:
    raise

 