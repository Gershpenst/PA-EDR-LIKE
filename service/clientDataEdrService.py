import requests,os,sys,inspect,uuid
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

parentdir = os.path.dirname(currentdir+"/../dao/")
sys.path.insert(0,parentdir)

from clientDataEdrDAO import createDataEdrDAO, getDataEdrDAO, getChangeHashWithPathFileDAO

parentdir = os.path.dirname(currentdir+"/../tools/")
sys.path.insert(0,parentdir)
from response import bodyMessageError, bodyMessageValid
from timestamp import getTimestampNow

VALID_DATA_TYPE = ["HASH_FILE", "REG_KEY"]

########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
# Reformatage des données envoyées
########################################################################################################################################
########################################################################################################################################
########################################################################################################################################


def __reformateGetDataEdr(data_edr):
    get_data_edr = []
    min_max = {}

    if "id" in data_edr:
        get_data_edr.append({"_id" : { "$eq" : data_edr["id"]}})
    if "data_type" in data_edr:
        if data_edr["data_type"] not in VALID_DATA_TYPE:
            return bodyMessageError("La donnée 'data_type' devrait être un des mots clés suivant : {}".format(", ".join(VALID_DATA_TYPE))) 
        get_data_edr.append({"data_type" : { "$eq" : data_edr["data_type"]}})
    if "computer_windows_id" in data_edr:
        get_data_edr.append({"computer_windows_id" : { "$eq" : data_edr["computer_windows_id"]}})

    if "min" in data_edr:
        min_max["$gte"] = int(data_edr["min"])
    if "max" in data_edr:
        min_max["$lte"] = int(data_edr["max"])

    if len(min_max) > 0:
        get_data_edr.append({"created_timestamp" : min_max})

    return bodyMessageValid(get_data_edr)


def __reformateCreateDataEdr(data_edr):
    return {
        "_id": uuid.uuid4().hex,
        "data_type": data_edr["data_type"],
        "computer_windows_id": data_edr["mac_addr"],
        "created_timestamp": getTimestampNow(),
        "data": data_edr["data"]
    }


def __reformateCreateDataForHashVTFile(data):
    try:
        return bodyMessageValid({
            "hash_id": data["hash_id"],
            "path_file": data["path_file"]
        })
    except KeyError as k:
        print("[__reformateCreateDataForHashVTFile] La donnée {} n'a pas été spécifié dans 'data'.".format(k))
        return bodyMessageError("La donnée {} n'a pas été spécifié dans 'data'.".format(k))
    except Exception as e:
        print("[__reformateCreateDataForHashVTFile] Erreur : {}".format(e))
        return bodyMessageError("Une erreur est survenue.") 


########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
# Verification des données
########################################################################################################################################
########################################################################################################################################
########################################################################################################################################


def verificationDataType(data_edr):
    data_type = data_edr["data_type"]
    if data_type not in VALID_DATA_TYPE:
        return bodyMessageError("La donnée 'data_type' devrait être un des mots clés suivant : {}".format(", ".join(VALID_DATA_TYPE))) 
    
    if data_type == VALID_DATA_TYPE[0]:
        data_reformate = __reformateCreateDataForHashVTFile(data_edr["data"])
        return data_reformate
    # A implémenter
    # elif data_type == VALID_DATA_TYPE[1]:
    return bodyMessageValid(data_edr["data"])


########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
# Les services à utiliser dans les API
########################################################################################################################################
########################################################################################################################################
########################################################################################################################################

def createDataEdrService(data_edr):
    try:
        data_reformate_with_type = verificationDataType(data_edr)
        if not data_reformate_with_type["success"]:
            return data_reformate_with_type
        data_edr["data"] = data_reformate_with_type["body"]

        reformate_create_data_edr = __reformateCreateDataEdr(data_edr)
        create_data_edr = createDataEdrDAO(reformate_create_data_edr)

        return bodyMessageValid(reformate_create_data_edr)
    except KeyError as k:
        print("[createDataEdrService] La donnée {} n'a pas été spécifié.".format(k))
        return bodyMessageError("La donnée {} n'a pas été spécifié.".format(k))
    except Exception as e:
        print("[createDataEdrService] Erreur : {}.".format(e))
        return bodyMessageError("Une erreur est survenue.")

def getDataEdrService(data_edr):
    try:
        reformate_data_get_edr = __reformateGetDataEdr(data_edr)
        if not reformate_data_get_edr["success"]:
            return reformate_data_get_edr

        get_data_edr = getDataEdrDAO(reformate_data_get_edr["body"])
        return bodyMessageValid(get_data_edr)
    except KeyError as k:
        print("[getDataEdrService] La donnée {} n'a pas été spécifié.".format(k))
        return bodyMessageError("La donnée {} n'a pas été spécifié.".format(k))
    except Exception as e:
        print("[getDataEdrService] Erreur : {}.".format(e))
        return bodyMessageError("Une erreur est survenue.")


def getChangeHashWithPathFileService(data):
    try:
        return getChangeHashWithPathFileDAO(data)
    except KeyError as k:
        print("[getChangeHashWithPathFileService] La donnée {} n'a pas été spécifié.".format(k))
        return bodyMessageError("La donnée {} n'a pas été spécifié.".format(k))
    except Exception as e:
        print("[getChangeHashWithPathFileService] Erreur : {}.".format(e))
        return bodyMessageError("Une erreur est survenue.")