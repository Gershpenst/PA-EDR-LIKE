import requests,os,sys,inspect,uuid
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir+"/../tools/")
sys.path.insert(0,parentdir)

from mongodbConn import instanceMongodb

PA_WINDOWS_CLIENT = instanceMongodb()["PA_EDR"]["PA_WINDOWS_CLIENT"]

def createWindowsClientDAO(windows_client_data):
    return PA_WINDOWS_CLIENT.insert_one(windows_client_data)

def getWindowsClientDAO(windows_client_id):
    data_windows_client =  PA_WINDOWS_CLIENT.find({
        "$or" : [{
            "_id" : { "$eq" : windows_client_id}
        },
        {
            "pc_name" : { "$eq" : windows_client_id}
        }]
    })
    return [dwc for dwc in data_windows_client]

def getAllWindowsClientDAO():
    find_all_client = PA_WINDOWS_CLIENT.find()
    return [fac for fac in find_all_client]