from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
import reconocimiento
import base_de_datos
#import led

cred = credentials.Certificate("reconocimiento-facial-amst-firebase-adminsdk-vtjii-da3f9f7588.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
#led.rojo(1)

print("base_de_datos.carpeta()")
path = base_de_datos.crear_fichero("C:/Users/Bruno/Pictures/amst/clase")

print("base_de_datos.extraer_datos()")
dic_nom, dic_asis = base_de_datos.extraer_datos(db, path)

print("reconocimiento.filtrar()")
reconocimiento.filtrar(path)

print("reconocimiento.entrenar()")
reconocimiento.entrenar(path)

print("reconocimiento.reconocimiento()")
reconocimiento.reconocimiento(db, path, dic_nom, dic_asis)