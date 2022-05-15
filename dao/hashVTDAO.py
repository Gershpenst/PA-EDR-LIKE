import requests,os,sys,inspect,uuid
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir+"/../tools/")
sys.path.insert(0,parentdir)

from mongodbConn import instanceMongodb

PA_CLIENT_HASH = instanceMongodb()["PA_EDR"]["PA_VT_HASH"]


def createHashVTDAO(data_vt):
    return PA_CLIENT_HASH.insert_one(data_vt)


def getHashVTDAO(hash_id):
    data_hash_vt =  PA_CLIENT_HASH.find({
        "$or" : [{
            "_id" : { "$eq" : hash_id}
        },
        {
            "md5" : { "$eq" : hash_id}
        },
        {
            "sha1" : { "$eq" : hash_id}
        },
        {
            "sha256" : { "$eq" : hash_id}
        }]
    })
    return [dhv for dhv in data_hash_vt]