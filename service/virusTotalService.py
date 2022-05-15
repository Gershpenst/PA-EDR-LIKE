import requests,os,sys,inspect,uuid
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir+"/")
sys.path.insert(0,parentdir) 
from hashVTService import createHashVTService, getHashVTService

parentdir = os.path.dirname(currentdir+"/../tools/")
sys.path.insert(0,parentdir) 

from response import bodyMessageError, bodyMessageValid
from timestamp import getTimestampNow

parentdir = os.path.dirname(currentdir+"/../api/")
sys.path.insert(0,parentdir) 
from virusTotalApi import getReportFromHashFileVTAPI


def __reformateDataVirusTotal(data):
    try:
        attributes = {} if "attributes" not in data else data["attributes"]
        return bodyMessageValid({
            "_id": data["id"],
            "name": attributes.get("meaningful_name", "N/A"),
            "type_vt": data.get("type", "N/A"),
            "total_votes": attributes.get("total_votes", {}),
            "size_file": attributes.get("size", "N/A"),
            "links": data.get("links", {}),
            "last_analysis_results": attributes.get("last_analysis_results", {}),
            "md5": attributes.get("md5", "N/A"),
            "sha1": attributes.get("sha1", "N/A"),
            "sha256": attributes.get("sha256", "N/A"),
            "trid": attributes.get("trid", []),
            "signature_info": attributes.get("signature_info", {}),
            "crowdsourced_yara_results": attributes.get("crowdsourced_yara_results", []),
        })
    except KeyError as k:
        print("[__reformateDataVirusTotal] reformate_data : {}".format(k))
        return bodyMessageError("La donnée {} n'a pas été spécifié.".format(k))
    except Exception as e:
        print("[__reformateDataVirusTotal] Error : {}".format(e))
        return bodyMessageError("Une erreur est survenue.")

def getReportFromHashFileVTService(data):
    try:
        data_hash = data["hash"]
        get_hash_local_vt = getHashVTService(data_hash)
        if get_hash_local_vt["success"]:
            return get_hash_local_vt

        get_format_hash_vt = getReportFromHashFileVTAPI(data_hash)
        if "data" in get_format_hash_vt:
            reformate_data = __reformateDataVirusTotal(get_format_hash_vt["data"])
            print("[getReportFromHashFileVTService] reformate_data ---> {}".format(reformate_data))

            if reformate_data["success"]:
                create_data_hash_vt = createHashVTService(reformate_data["body"])
                print("[getReportFromHashFileVTService] Found in VT ---> {}".format(create_data_hash_vt))
            return reformate_data

        reformate_data = __reformateDataVirusTotal({"id": data_hash})
        create_data_hash_vt = createHashVTService(reformate_data["body"])
        print("[getReportFromHashFileVTService] Not found in VT ---> {}".format(create_data_hash_vt))
        return reformate_data
    except KeyError as k:
        print("[getReportFromHashFileVTService] La donnée {} n'a pas été trouvée.".format(k))
        return bodyMessageError("La donnée {} n'a pas été trouvée.".format(k))
    except Exception as e:
        print("[getReportFromHashFileVTService] Error : {}".format(e))
        return bodyMessageError("Une erreur est survenue.")