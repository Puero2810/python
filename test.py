from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin

cred = credentials.Certificate("reconocimiento-facial-amst-firebase-adminsdk-vtjii-da3f9f7588.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

docs = db.collection(u'usuario').stream()
dic = {}
for doc in docs:
    if (doc.to_dict()["tipo"] == "estudiante"):
        dic[doc.id] = doc.to_dict()["asistencias"]
dic2 = dic['201709920']
dic2['26/01/2023'] = True
dic['201709920'] = dic2
print(dic)
#lista = {"22/01/2023": "False"}
#db.collection(u"usuario").document(u"201709920").update({"asistencias": lista})