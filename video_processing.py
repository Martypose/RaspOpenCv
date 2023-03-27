import cv2 as cv
import numpy as np
import time
from socketio_handling import esta_conectado  # Importa cliente_conectado


def resize_min(imagen, imagen_fondo):
    h1, w1 = imagen.shape[:2]
    h2, w2 = imagen_fondo.shape[:2]

    # Encuentra el mínimo ancho y alto
    #min_ancho = min(w1, w2)
    #min_alto = min(h1, h2)

    # Redimensiona ambas imágenes al tamaño mínimo
    #imagen_resized = cv.resize(imagen, (min_ancho, min_alto))
    #imagen_fondo_resized = cv.resize(imagen_fondo, (min_ancho, min_alto))

    return imagen_resized, imagen_fondo_resized

def detectar_objetos(imagen):
    # Redimensionar ambas imágenes al tamaño mínimo
    #imagen, imagen_fondo = resize_min(imagen, imagen_fondo)
    
    # Convertir la imagen de BGR a HSV
    hsv = cv.cvtColor(imagen, cv.COLOR_BGR2HSV)
    
    # Convertir la imagen_fondo de BGR a HSV
    #hsv_fondo = cv.cvtColor(imagen_fondo, cv.COLOR_BGR2HSV)

    # Restar la imagen_fondo de la imagen
    # hsv = cv.subtract(hsv, hsv_fondo)

    #cv.imwrite("fondorestado.png",hsv)

    # Tomar el canal de saturación
    sat = hsv[:,:,2]
    grises = sat

    # Aplicar un desenfoque gaussiano
    grises = cv.GaussianBlur(grises, (3,3), 0)
    
    # Binarizar la imagen con un umbral
    binarizacion_global = cv.threshold(grises, 200, 255, cv.THRESH_BINARY)[1]

    cv.imwrite("binarizada.png",binarizacion_global)
    # Dilatar y erosionar la imagen para eliminar ruido
    kernel = np.ones((3,3), np.uint8)
    dilate = cv.dilate(binarizacion_global, kernel, iterations=1)

    erode = cv.erode(dilate, kernel, iterations=1)
    dilate = cv.erode(erode, kernel, iterations=1)
    erode = cv.erode(dilate, kernel, iterations=1)

    # Aplicar una apertura morfológica para eliminar pequeños objetos
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (13, 13))
    opening = cv.morphologyEx(erode, cv.MORPH_OPEN, kernel, iterations=4)

    # Encontrar contornos en la imagen
    cnts, _ = cv.findContours(opening, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    print('He aplicado transformaciones morfologicas a la imagen')
    return cnts

# Función para guardar medidas de los objetos detectados y enviarlas a través de socketio
def guardar_medidas(contornos,socketio,imagen ):
    medidas = []
    
    imagencopia = imagen.copy()
    

    # Iterar sobre los contornos encontrados
    for c in contornos:
        area = cv.contourArea(c)
        x, y, w, h = cv.boundingRect(c)
        # x es la posición horizontal, y es la posición vertical
        # w es el ancho, h es la altura
        aspect_ratio = float(w) / h

        # Filtrar objetos basándose en su relación de aspecto, altura y posición horizontal
        if aspect_ratio > 3 and 100 < h < 200 and x > 200:
            # Aqui se meten las medidas de cada tabla en una lista
            # Normalmente hay una tabla solo, pero por si acaso
            # Si hay más de una tabla, se envían todas, se tratará
            
            print("Medidas: ",w, h)
            medidas.append((w, h))
            rect = cv.minAreaRect(c)
            box = cv.boxPoints(rect)
            box = np.intp(box)
            cv.drawContours(imagencopia,[box],0,(24,255,12),3)
    cv.imwrite("imagendetectada.png",imagencopia)

    # Enviar las medidas a través de socketio
    # Espera a que el cliente se conecte antes de enviar las medidas
    while not esta_conectado():
        time.sleep(0.1)
    
    enviar_medidas(medidas, socketio)

# Función principal para procesar el video de la cámara
def procesar_video(captura, socketio):
    
    # Definir las nuevas dimensiones
    nuevo_ancho = 320
    nuevo_alto = 240
    
    frame_anterior = None
    tiempo_espera = 2
    tiempo_ultimo_cambio = 0
    procesar_siguiente_frame = False
    umbral_movimiento = 248022  # Ajusta este valor para cambiar la sensibilidad

    while True:
        frame = captura.capture_array()
	# Guarda la imagen capturada en un archivo
        cv.imwrite("captura.png", frame)
	        
            # Redimensionar el frame
        #frame = cv.resize(frame, (nuevo_ancho, nuevo_alto))
        contornos = detectar_objetos(frame)
        guardar_medidas(contornos, socketio,frame)
 #       procesar_siguiente_frame = False
        # Guardar el frame actual como frame anterior para la siguiente iteración
#        frame_anterior = frame.copy()

        # Mostrar el frame en una ventana
        # cv.imshow("Resultado", frame)

        # Salir del bucle si se presiona la tecla 'q'
        if cv.waitKey(1) & 0xFF == ord("q"):
            break


def procesar_imagen(imagen,fondo, socketio):
    # ancho de la imagen
    ancho = imagen.shape[1]
    # alto de la imagen
    alto = imagen.shape[0]
    # Redimensionar el frame
    print("ancho: ", ancho)
    print("alto: ", alto)
    while True:
        contornos = detectar_objetos(imagen,fondo)
        guardar_medidas(contornos, socketio, imagen)
        time.sleep(1)  # Espera 3 segundos antes de procesar la imagen nuevamente
    
def enviar_medidas(medidas, socketio):
    print('Enviando medidas al servidor nodejs')
    socketio.emit("medidas", medidas)
