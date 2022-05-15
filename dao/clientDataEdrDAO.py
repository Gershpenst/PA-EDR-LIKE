import requests,os,sys,inspect,uuid
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir+"/../tools/")
sys.path.insert(0,parentdir)

from mongodbConn import instanceMongodb

PA_DATA_EDR = instanceMongodb()["PA_EDR"]["PA_DATA_EDR"]

def createDataEdrDAO(data_edr):
    return PA_DATA_EDR.insert_one(data_edr)

def getDataEdrDAO(data_edr):
    data_edr =  PA_DATA_EDR.find({"$and" : data_edr}) if len(data_edr) > 0 else PA_DATA_EDR.find()
    return [de for de in data_edr]

### Permet de regrouper le "hash_id" et "path_file" afin de voir quels sont les hashs qui ont changés en fonction des chemins
def getChangeHashWithPathFileDAO(data):
    match_data_edr = {"data_type" : "HASH_FILE"}
    if "computer_windows_id" in data:
        match_data_edr["computer_windows_id"] = data["computer_windows_id"]

    data_edr = PA_DATA_EDR.aggregate([
        {"$match" : match_data_edr},
        { "$group": {
            "_id": {
                "hash_id": "$data.hash_id",
                "path_file": "$data.path_file"
            },
            "created_timestamp_first": { "$first": "$created_timestamp" },
            "created_timestamp_last": { "$last": "$created_timestamp" },
            "count": { "$sum": 1 }
        }}
    ])
    return [de for de in data_edr]