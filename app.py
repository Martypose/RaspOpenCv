from flask import Flask
import threading
import cv2 as cv
from video_processing import procesar_video, procesar_imagen
from resource_monitoring import enviar_estadisticas
from socketio_handling import sio, connect, disconnect, esta_conectado

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

def main():
    # Cargar la imagen desde un archivo
    imagen = cv.imread("tabla5.png")

    if imagen is None:
        print("Error al cargar la imagen.")
        return
    
    try:
        # Procesa la imagen (en lugar de capturar y procesar video)
        imagen_thread = threading.Thread(target=procesar_imagen, args=(imagen, sio))  # Cambio de socketio a sio
        imagen_thread.start()
        # Inicia el hilo de envío de estadísticas
        stats_thread = threading.Thread(target=enviar_estadisticas, args=(sio,))
        stats_thread.start()

        # Ejecuta la aplicación Flask en el hilo principal
        app.run(host="0.0.0.0", port=5000)

    finally:
        pass

if __name__ == "__main__":
    main()