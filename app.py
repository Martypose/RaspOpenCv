from flask import Flask
from flask_socketio import SocketIO
import threading
import cv2 as cv
from video_processing import procesar_video
from resource_monitoring import enviar_estadisticas
from socketio_handling import handle_connect, handle_disconnect

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")

socketio.on_event("connect", handle_connect)
socketio.on_event("disconnect", handle_disconnect)

def main():
    captura = cv.VideoCapture(0)
    if not captura.isOpened():
        print("Error al abrir la cámara.")
        return

    try:
        # Inicia el hilo de procesamiento de video
        video_thread = threading.Thread(target=procesar_video, args=(captura, socketio))
        video_thread.start()

        # Inicia el hilo de envío de estadísticas
        stats_thread = threading.Thread(target=enviar_estadisticas, args=(socketio,))
        stats_thread.start()

        # Ejecuta la aplicación Flask-SocketIO en el hilo principal
        socketio.run(app, host="0.0.0.0", port=5000)

    finally:
        captura.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    main()
