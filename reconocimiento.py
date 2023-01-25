import base_de_datos
import numpy as np
import datetime
#import lcd
#import led
import cv2
import os

def filtrar(path):
     clasificar_rostro = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
     conteo = 0
     for nombre_imagen in os.listdir(path):
          imagen = cv2.imread(path + "/" + nombre_imagen)
          rostros = clasificar_rostro.detectMultiScale(imagen, 1.1, 5)
          for (x, y, w, h) in rostros:
               cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 255, 0), 2)
               rostro = imagen[y:y + h, x:x + w]
               rostro = cv2.resize(rostro, (150, 150))
               path1 = base_de_datos.crear_fichero(path + "/" + nombre_imagen.replace(".jpg", ""))
               cv2.imwrite(path1 + "/" + nombre_imagen.replace(".jpg", "") + "-" + str(conteo) + ".jpg", rostro)
               conteo += 1

          base_de_datos.eliminar_fichero(path + "/" + nombre_imagen)

def entrenar(path):
     lista_personas = os.listdir(path)
     datos_rostros = []
     etiquetas = []
     etiqueta = 0

     for nombre_carpeta in lista_personas:
          path_persona = path + '/' + nombre_carpeta
          for fileName in os.listdir(path_persona):
               etiquetas.append(etiqueta)
               datos_rostros.append(cv2.imread(path_persona + '/' + fileName, 0))
          etiqueta += 1

     reconocedor_rostro = cv2.face.EigenFaceRecognizer_create()
     reconocedor_rostro.train(datos_rostros, np.array(etiquetas))
     reconocedor_rostro.write(path + 'modeloEigenFace.xml')

def reconocimiento(db, path, dic_nom, dic_asis):
     path_imagenes = os.listdir(path)
     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
     clasificar_rostro = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
     reconocedor_rostro = cv2.face.EigenFaceRecognizer_create()
     reconocedor_rostro.read(path + 'modeloEigenFace.xml')

     while True:
          ret, frame = cap.read()

          if ret == False: break

          color = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
          aux = color.copy()
          rostros = clasificar_rostro.detectMultiScale(color, 1.3, 5)
          for (x, y, w, h) in rostros:
               rostro = aux[y:y + h, x:x + w]
               rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
               result = reconocedor_rostro.predict(rostro)
               cv2.putText(frame, '{}'.format(result), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
               if result[1] < 5700:
                    print(path_imagenes[result[0]])
                    for key in dic_nom:
                         if path_imagenes[result[0]] == dic_nom[key]:
                              fecha = datetime.datetime.now()
                              dia = fecha.day
                              mes = fecha.month
                              ano = fecha.year
                              fecha = str(dia) + "/" + str(mes) + "/" + str(ano)
                              base_de_datos.enviar_datos(db, key, fecha, True, dic_asis)
                              #lcd.nombre(dic_nom[key])
                              #led.verde(1, 2)

          cv2.imshow('frame', frame)
          k = cv2.waitKey(1)
          if k == 27: break

     cap.release()
     cv2.destroyAllWindows()