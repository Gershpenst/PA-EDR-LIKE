from pymongo.errors import DuplicateKeyError

import requests,os,sys,inspect,uuid
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir+"/../dao/")
sys.path.insert(0,parentdir)

from computerWindowsDAO import createWindowsClientDAO, getWindowsClientDAO, getAllWindowsClientDAO

parentdir = os.path.dirname(currentdir+"/../tools/")
sys.path.insert(0,parentdir)

from response import bodyMessageError, bodyMessageValid

def __reformateWindowsClient(windows_client_data):
    return {
        "_id": windows_client_data["mac_addr"],
        "pc_name": windows_client_data["pc_name"],
        "username": windows_client_data["username"]
    }

def createWindowsClientService(data_windows_client):
    try:
        reformate_create_windows_client = __reformateWindowsClient(data_windows_client)
        create_hash_service = createWindowsClientDAO(reformate_create_windows_client)
        return bodyMessageValid(data_windows_client)
    except DuplicateKeyError as dke:
        print("[createWindowsClientService] L'id {} est déjà présent dans la table.".format(reformate_create_windows_client["_id"]))
        return bodyMessageError("L'id {} est déjà présent dans la table.".format(reformate_create_windows_client["_id"]))
    except KeyError as k:
        print("[createWindowsClientService] La donnée {} n'a pas été spécifié.".format(k))
        return bodyMessageError("La donnée {} n'a pas été spécifié.".format(k))
    except Exception as e:
        print("[createWindowsClientService] La donnée {} n'a pas été spécifié.".format(e))
        return bodyMessageError("Une erreur est survenue.")

def getWindowsClientService(windows_client_id):
    try:
        get_windows_client = getWindowsClientDAO(windows_client_id)
        if len(get_windows_client) <= 0:
            return bodyMessageError("L'utilisateur {} n'existe pas.".format(windows_client_id))
        return bodyMessageValid(get_windows_client)
    except KeyError as k:
        print("[getWindowsClientService] La donnée {} n'a pas été spécifié.".format(k))
        return bodyMessageError("La donnée {} n'a pas été spécifié.".format(k))
    except Exception as e:
        print("[getWindowsClientService] La donnée {} n'a pas été spécifié.".format(e))
        return bodyMessageError("Une erreur est survenue.")

def getAllWindowsClientService():
    try:
        get_all_client = getAllWindowsClientDAO()
        if len(get_all_client) <= 0:
            return bodyMessageError("La base de donnée est vide.")
        return bodyMessageValid(get_all_client)
    except KeyError as k:
        print("[getAllWindowsClientService] La donnée {} n'a pas été spécifié.".format(k))
        return bodyMessageError("La donnée {} n'a pas été spécifié.".format(k))
    except Exception as e:
        print("[getAllWindowsClientService] La donnée {} n'a pas été spécifié.".format(e))
        return bodyMessageError("Une erreur est survenue.")