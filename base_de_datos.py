import requests
import os

# Creacion de carpeta
def crear_fichero(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    return path

# Extraer data de la base de datos
def extraer_datos(db, path):
    dic_nom = {}
    dic_asis = {}
    docs = db.collection(u'usuario').stream()
    for doc in docs:
        if(doc.to_dict()["tipo"] == "estudiante"):
            dic_asis[doc.id] = doc.to_dict()["asistencias"]
            dic_nom[doc.id] = doc.to_dict()["nombre"] + " " + doc.to_dict()["apellido"]
            imagen = requests.get(doc.to_dict()["foto"]).content
            with open(path + "/" + doc.to_dict()["nombre"]+" "+doc.to_dict()["apellido"] + ".jpg", 'wb') as handler:
                handler.write(imagen)

    return dic_nom, dic_asis

# Eliminacion de ficheros
def eliminar_fichero(path):
    os.remove(path)

# Enviar data a la base de datos
def enviar_datos(db, matricula, fecha, bool, dic_asis):
    dic = dic_asis[matricula]
    dic[fecha] = bool
    dic_asis[matricula] = dic
    db.collection(u"usuario").document(matricula).update({"asistencias":dic_asis[matricula]})