from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import json
from waitress import serve
import requests
import datetime
import re

app=Flask(__name__)
app.config["JWT_SECRET_KEY"]="super-secret"#cambiar por  el se convierte
jwt=JWTManager(app)
cors=CORS(app)

@app.before_request#Hace primero esta logica antes de consumir un servicio rest
def middleware():
    url_cliente=request.path#obtiene el path al servicio que quiere acceder
    metodo_cliente=request.method#para saber que metodo esta apuntando
    if(url_cliente=="/login"):
        pass
    elif verify_jwt_in_request():#valida que se haya enviado un token,  que sea enviado de la misma aplicacion, entre otras funciones:

        infoToken=get_jwt_identity()#obtiene la informacion del usuario,formato json
        idRol=infoToken["rol"]["_id"]
        if(idRol==None):
            print("no tiene roles asociados")
        url_cliente=transformarUrl(url_cliente)
        urlValidarPermis=dataConfig["url-backend-proyecto-mintic-seguridad"]+"/permisosRol/validar-permisos/rol/"+idRol
        headers = {"Content-Type": "application/json"}
        bodyRequest={
            "url":url_cliente,
            "metodo": metodo_cliente
        }
        responseValidarPermiso=requests.get(urlValidarPermis,json=bodyRequest,headers=headers)
        print(responseValidarPermiso)
        if(responseValidarPermiso.status_code==200):
            print("El cliente tiene permisos")
            pass
        else:
            return{"mensaje":"Permiso denegado"},401
def transformarUrl(urlCliente):

    listadoUrl=urlCliente.split("/")
    for x in listadoUrl:
        if re.search('\\d',x):
            urlCliente=urlCliente.replace(x,"?")
    return urlCliente




@app.route("/login",methods=["POST"])
def validarUsuario():
    url=dataConfig["url-backend-proyecto-mintic-seguridad"]+"/usuarios/validar-usuario"
    headers ={"Content-Type":"application/json"}
    bodyRequest=request.get_json()
    response=requests.post(url,json=bodyRequest,headers=headers)#consume un servicio rest
    if(response.status_code==200):
        print("El usuario se valido correctamente")
        infoUsuario=response.json()
        TiempoDelToken=datetime.timedelta(seconds=60*60)
        newToken=create_access_token(identity=infoUsuario,expires_delta=TiempoDelToken)
        return {"token":newToken}
    else:
        return {"Mensaje": "Usuario y contraseña Erroneos"},401

#--------------------------------------------------------------------------------------------------------------
#metodos de Mesa
#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#creacion de mesa
#--------------------------------------------------------------------------------------------------------------
@app.route("/mesa", methods=['POST'])
def crearMesa():
    url = dataConfig["url-backend-proyecto-mintic"] + "/mesa"
    body = request.get_json()
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=body,headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------
#metodos de obtencion de datos
#--------------------------------------------------------------------------------------------------------------
@app.route("/mesa", methods=['GET'])
def GETMesa():
    url = dataConfig["url-backend-proyecto-mintic"] + "/mesa"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()

@app.route("/mesa/<string:idObject>", methods=['GET'])
def GETMesas(idObject):
    url = dataConfig["url-backend-proyecto-mintic"] + "/mesa/" + idObject
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------
#metodo de actualizacion
#--------------------------------------------------------------------------------------------------------------
@app.route("/mesa", methods=['PUT'])
def PutMesa():
    url = dataConfig["url-backend-proyecto-mintic"] + "/mesa"
    body = request.get_json()
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, json=body, headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------
#metodo borrar
#--------------------------------------------------------------------------------------------------------------
@app.route("/mesa/<string:idObject>", methods=['DELETE'])
def DeleteMesa(idObject):
    url = dataConfig["url-backend-proyecto-mintic"] + "/mesa/" + idObject
    headers = {"Content-Type": "application/json"}
    response = requests.delete(url, headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#metodos de Candidato
#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#creacion de mesa
#--------------------------------------------------------------------------------------------------------------
@app.route("/candidato",methods=["POST"])
def crearCandidato():
    url=dataConfig["url-backend-proyecto-mintic"]+"/candidato"
    headers={"Content-Type":"application/json"}
    body=request.get_json()
    response=requests.post(url,json=body,headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------
#metodos de obtencion de datos
#--------------------------------------------------------------------------------------------------------------
@app.route("/candidato", methods=['GET'])
def GETtodosCandidato():
    url=dataConfig["url-backend-proyecto-mintic"]+"/candidato"
    headers={"Content-Type":"application/json"}
    response=requests.get(url,headers=headers)
    return response.json()
@app.route("/candidato/<string:idObject>", methods=['GET'])
def GETCandidato(idObject):
    url = dataConfig["url-backend-proyecto-mintic"] + "/candidato/"+idObject
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------
#metodo de actualizacion
#--------------------------------------------------------------------------------------------------------------
@app.route("/candidato", methods=['PUT'])
def PutCandidato():
    url = dataConfig["url-backend-proyecto-mintic"] + "/candidato"
    headers = {"Content-Type": "application/json"}
    body = request.get_json()
    response = requests.put(url, json=body, headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------
#metodo de asignacion partido
#--------------------------------------------------------------------------------------------------------------
@app.route("/candidato/<string:idCandidato>/partido/<string:idPartido>", methods=['PUT'])
def AsignarPartidoCandidato(idCandidato, idPartido):
    url = dataConfig["url-backend-proyecto-mintic"] + "/candidato/"+idCandidato+"/partido/"+idPartido
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------
#metodo borrar
#--------------------------------------------------------------------------------------------------------------
@app.route("/candidato/<string:idObject>", methods=['DELETE'])
def DeleteCandidato(idObject):
    url = dataConfig["url-backend-proyecto-mintic"] + "/candidato/" + idObject
    headers = {"Content-Type": "application/json"}
    response = requests.delete(url, headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#metodos de Partido
#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#creacion de Partido
#--------------------------------------------------------------------------------------------------------------
@app.route("/partido", methods=['POST'])
def crearPartido():
    url = dataConfig["url-backend-proyecto-mintic"] + "/partido"
    headers = {"Content-Type": "application/json"}
    body = request.get_json()
    response = requests.post(url, json=body, headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------
#Obtencion de datos
#--------------------------------------------------------------------------------------------------------------
@app.route("/partido", methods=['GET'])
def GETPartido():
    url = dataConfig["url-backend-proyecto-mintic"] + "/partido"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()
@app.route("/partido/<string:idObject>", methods=['GET'])
def GETtodosPartidos(idObject):
    url = dataConfig["url-backend-proyecto-mintic"] + "/partido/" + idObject
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------
#metodo de actualizacion
#--------------------------------------------------------------------------------------------------------------
@app.route("/partido", methods=['PUT'])
def PutPartido():
    url = dataConfig["url-backend-proyecto-mintic"] + "/partido"
    headers = {"Content-Type": "application/json"}
    body = request.get_json()
    response = requests.put(url, json=body, headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------
#metodo borrar
#--------------------------------------------------------------------------------------------------------------
@app.route("/partido/<string:idObject>", methods=['DELETE'])
def DeletePartido(idObject):
    url = dataConfig["url-backend-proyecto-mintic"] + "/partido/" + idObject
    headers = {"Content-Type": "application/json"}
    response = requests.delete(url, headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#metodos de Resultado
#--------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------
#creacion de Resultado
#--------------------------------------------------------------------------------------------------------------

@app.route("/resultado/candidato/<string:idCandidato>/mesa/<string:idMesa>", methods=['POST'])
def crearResultado(idCandidato, idMesa):
    url = dataConfig["url-backend-proyecto-mintic"] + "/resultado/candidato/"+idCandidato+"/mesa/"+idMesa
    headers = {"Content-Type": "application/json"}
    body = request.get_json()
    print(body)
    response = requests.post(url, json=body, headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------
#Obtencion de datos
#--------------------------------------------------------------------------------------------------------------
@app.route("/resultado", methods=['GET'])
def GETResultado():
    url = dataConfig["url-backend-proyecto-mintic"] + "/resultado"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()
@app.route("/resultado/<string:idObject>", methods=['GET'])
def GETPartidos(idObject):
    url = dataConfig["url-backend-proyecto-mintic"] + "/resultado/" + idObject
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------
#metodo de actualizacion
#--------------------------------------------------------------------------------------------------------------
@app.route("/resultado", methods=['PUT'])
def PutResultado():
    url = dataConfig["url-backend-proyecto-mintic"] + "/resultado"
    headers = {"Content-Type": "application/json"}
    body = request.get_json()
    response = requests.put(url, json=body, headers=headers)
    return response.json()
#--------------------------------------------------------------------------------------------------------------
#metodo borrar
#--------------------------------------------------------------------------------------------------------------
@app.route("/resultado/<string:idObject>", methods=['DELETE'])
def DeleteResultado(idObject):
    url = dataConfig["url-backend-proyecto-mintic"] + "/resultado/" + idObject
    headers = {"Content-Type": "application/json"}
    response = requests.delete(url, headers=headers)
    return response.json()

def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dataConfig = loadFileConfig()
    print("Server running : " + "http://" + dataConfig["url-backend"] + ":" + str(dataConfig["port"]))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])
