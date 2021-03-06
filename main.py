import json,requests,os,ssl,sys,inspect

from flask import Flask, jsonify, request
from flask_cors import CORS

from env.server_env import HOSTNAME_FLASK, PORT_FLASK, SECURE_MODE, VERIFIED_USER

from tools.response import bodyMessageError, bodyMessageValid

from service.virusTotalService import getReportFromHashFileVTService

from internalEdrApi import  createWindowsClientApi, getWindowsClientApi, getAllWindowsClientApi, \
                            createDataEdrApi, getDataEdrApi, getChangeHashWithPathFileApi

app = Flask(__name__)
CORS(app)

@app.route('/info/vt', methods=['GET'])
def getReportVT():
    hash_data = request.args.get('hash', type=str)
    print("hash_data --> {}".format(hash_data))
    if hash_data == None:
        return jsonify(bodyMessageError("La donnée hash n'a pas été spécifié dans l'url."))
    get_report_hash = getReportFromHashFileVTService({"hash": hash_data})
    return jsonify(get_report_hash)


@app.route('/client/<mac_addr>', methods=['POST'])
def registerMachineWindowsClient(mac_addr):
    if not request.is_json:
        return jsonify(bodyMessageError("Le body n'est pas au format json."))
    content = request.json
    content["mac_addr"] = mac_addr
    print("content --> {}".format(mac_addr))

    create_windows_user = createWindowsClientApi(content)
    return jsonify(create_windows_user)

@app.route('/client/<mac_addr>', methods=['GET'])
def getMachineWindowsClient(mac_addr):
    get_windows_user = getWindowsClientApi(mac_addr)
    return jsonify(get_windows_user)

@app.route('/client', methods=['GET'])
def getAllMachineWindowsClient():
    get_all_windows_user = getAllWindowsClientApi()
    return jsonify(get_all_windows_user)


@app.route('/edr', methods=['POST'])
def createDataEdr():
    if not request.is_json:
        return jsonify(bodyMessageError("Le body n'est pas au format json."))
    content = request.json

    create_data_edr = createDataEdrApi(content)
    return jsonify(create_data_edr)

@app.route('/edr', methods=['GET'])
def getDataEdr():
    get_data_edr = getDataEdrApi(request.args)
    return jsonify(get_data_edr)


if __name__ == "__main__":
    context = None
    if SECURE_MODE:
        currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        parentdir = os.path.dirname(currentdir+"/certificate/")
        SERVER_CRT = "{}/server.crt".format(parentdir)
        SERVER_PRIV_KEY =  "{}/server.key".format(parentdir)
        CA_CRT = "{}/ca.crt".format(parentdir)
        
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        if VERIFIED_USER:
            context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(CA_CRT)
        context.load_cert_chain(SERVER_CRT, SERVER_PRIV_KEY)
    app.run(host=HOSTNAME_FLASK, port=int(PORT_FLASK), ssl_context=context)