from pymongo.errors import DuplicateKeyError

import requests,os,sys,inspect,uuid
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir+"/../dao/")
sys.path.insert(0,parentdir)

from hashVTDAO import createHashVTDAO, getHashVTDAO

parentdir = os.path.dirname(currentdir+"/../tools/")
sys.path.insert(0,parentdir)

from response import bodyMessageError, bodyMessageValid

def createHashVTService(data_vt):
    try:
        create_hash_service = createHashVTDAO(data_vt)
        return bodyMessageValid(data_vt)
    except DuplicateKeyError as dke:
        print("[createHashVTService] L'id {} est déjà présent dans la table.".format(data_vt["_id"]))
        return bodyMessageError("L'id {} est déjà présent dans la table.".format(data_vt["_id"]))
    except KeyError as k:
        print("[createHashVTService] La donnée {} n'a pas été spécifié.".format(k))
        return bodyMessageError("La donnée {} n'a pas été spécifié.".format(k))
    except Exception as e:
        print("[createHashVTService] La donnée {} n'a pas été spécifié.".format(k))
        return bodyMessageError("Une erreur est survenue.")

def getHashVTService(hash_id):
    try:
        get_hash_vt = getHashVTDAO(hash_id)
        if len(get_hash_vt) <= 0:
            return bodyMessageError("Aucune donnée trouvée.")
        return bodyMessageValid(get_hash_vt[0])
    except KeyError as k:
        print("[getHashVTService] La donnée {} n'a pas été spécifié.".format(k))
        return bodyMessageError("La donnée {} n'a pas été spécifié.".format(k))
    except Exception as e:
        print("[getHashVTService] La donnée {} n'a pas été spécifié.".format(k))
        return bodyMessageError("Une erreur est survenue.")