
import requests,os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir+"/../env/")
sys.path.insert(0,parentdir) 

from virustotal_env import URL_VT, API_TOKEN_VT

def getReportFromHashFileVTAPI(hash_file):
    url = "{}/files/{}".format(URL_VT, hash_file)

    headers = {
        "Accept": "application/json",
        "x-apikey": API_TOKEN_VT
    }

    response = requests.get(url, headers=headers)
    return response.json()
