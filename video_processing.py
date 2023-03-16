# video_processing.py

import cv2 as cv
import numpy as np
import time

def detectar_objetos(imagen):
    hsv = cv.cvtColor(imagen, cv.COLOR_BGR2HSV)
    sat = hsv[:,:,2]
    grises = sat

    grises = cv.GaussianBlur(grises, (3,3), 0)

    binarizacion_global = cv.threshold(grises, 200, 255, cv.THRESH_BINARY)[1]

    kernel = np.ones((3,3), np.uint8)
    dilate = cv.dilate(binarizacion_global, kernel, iterations=1)

    erode = cv.erode(dilate, kernel, iterations=1)
    dilate = cv.erode(erode, kernel, iterations=1)
    erode = cv.erode(dilate, kernel, iterations=1)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (13, 13))
    opening = cv.morphologyEx(erode, cv.MORPH_OPEN, kernel, iterations=4)

    cnts, _ = cv.findContours(opening, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return cnts

def guardar_medidas(contornos, socketio):
    medidas = []

    for c in contornos:
        area = cv.contourArea(c)
        x, y, w, h = cv.boundingRect(c)
        aspect_ratio = float(w) / h

        if aspect_ratio > 3 and 100 < h < 200 and x > 200:
            medidas.append((x, y, w, h))

    enviar_medidas(medidas, socketio)

def procesar_video(captura, socketio):
    frame_anterior = None
    tiempo_espera = 2
    tiempo_ultimo_cambio = 0
    procesar_siguiente_frame = False
    umbral_movimiento = 248022  # Ajusta este valor para cambiar la sensibilidad
    
    while True:
        ret, frame = captura.read()
        if not ret:
            break

        if frame_anterior is not None:
            diferencia = cv.absdiff(frame, frame_anterior)
            movimiento = cv.countNonZero(cv.cvtColor(diferencia, cv.COLOR_BGR2GRAY))
            

            if movimiento > umbral_movimiento:
                print(movimiento)
                tiempo_ultimo_cambio = time.time()
                procesar_siguiente_frame = True
            elif procesar_siguiente_frame and time.time() - tiempo_ultimo_cambio >= tiempo_espera:
                contornos = detectar_objetos(frame)
                guardar_medidas(contornos, socketio)
                procesar_siguiente_frame = False

        frame_anterior = frame.copy()

        cv.imshow("Resultado", frame)

        if cv.waitKey(1) & 0xFF == ord("q"):
            break

def enviar_medidas(medidas, socketio):
    print('Enviando medidas al servidor nodejs')
    socketio.emit("medidas", medidas)
