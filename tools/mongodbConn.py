import pymongo

import requests,os,sys,inspect,uuid
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir+"/../env/")
sys.path.insert(0,parentdir) 

from mongodb_env import MONGODB_DOMAIN, MONGODB_PORT, MONGODB_USERNAME, MONGODB_PASSWORD

# try to instantiate a client instance
def instanceMongodb():
    return pymongo.MongoClient(
        host = [ "{}:{}".format(MONGODB_DOMAIN, MONGODB_PORT) ],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
        username = MONGODB_USERNAME,
        password = MONGODB_PASSWORD
    )