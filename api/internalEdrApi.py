import requests,os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

parentdir = os.path.dirname(currentdir+"/../service/")
sys.path.insert(0,parentdir)

from computerWindowsService import createWindowsClientService, getWindowsClientService, getAllWindowsClientService
from clientDataEdrService import createDataEdrService, getDataEdrService, getChangeHashWithPathFileService
from virusTotalService import getReportFromHashFileVTService

parentdir = os.path.dirname(currentdir+"/../tools/")
sys.path.insert(0,parentdir)
from response import bodyMessageError

########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
# Gérer les utilisateurs Windows
########################################################################################################################################
########################################################################################################################################
########################################################################################################################################

def createWindowsClientApi(data):
    return createWindowsClientService(data)

def getWindowsClientApi(windows_client_id):
    return getWindowsClientService(windows_client_id)

def getAllWindowsClientApi():
    return getAllWindowsClientService()


########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
# Gérer les datas envoyés pour un utilisateur
########################################################################################################################################
########################################################################################################################################
########################################################################################################################################

def createDataEdrApi(data):
    try:
        get_windows_client = getWindowsClientApi(data["mac_addr"])
        if not get_windows_client["success"]:
            return get_windows_client

        hash_id = data["data"]
        hash_id = hash_id["hash_id"]
        get_report_vt_hash = getReportFromHashFileVTService({"hash": hash_id})

        return createDataEdrService(data)
    except KeyError as k:
        print("[createDataEdrApi] La donnée {} n'a pas été spécifié.".format(k))
        return bodyMessageError("La donnée {} n'a pas été spécifié.".format(k))
    except Exception as e:
        print("[createDataEdrApi] Erreur : {}.".format(e))
        return bodyMessageError("Une erreur est survenue.")


def getDataEdrApi(data):
    return getDataEdrService(data)

def getChangeHashWithPathFileApi(data):
    return getChangeHashWithPathFileService(data)