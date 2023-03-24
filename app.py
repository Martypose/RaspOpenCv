from flask import Flask
import threading
import cv2 as cv
from resource_monitoring import enviar_estadisticas
from socketio_handling import sio, connect, disconnect, esta_conectado
from video_processing import procesar_video, procesar_imagen

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

def main():
    captura = cv.VideoCapture(0)

    if not captura.isOpened():
        print("Error al abrir la cámara.")
        return

    try:
        # Procesa el video (en lugar de capturar y procesar una imagen)
        video_thread = threading.Thread(target=procesar_video, args=(captura, sio))  # Cambio de socketio a sio
        video_thread.start()
        # Inicia el hilo de envío de estadísticas
        stats_thread = threading.Thread(target=enviar_estadisticas, args=(sio,))
        stats_thread.start()

        # Ejecuta la aplicación Flask en el hilo principal
        app.run(host="0.0.0.0", port=5000)

    finally:
        captura.release()

if __name__ == "__main__":
    main()
