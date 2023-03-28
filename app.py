from flask import Flask
import threading
from picamera2 import Picamera2
from libcamera import controls
from resource_monitoring import enviar_estadisticas
from socketio_handling import sio, connect, disconnect, esta_conectado
from video_processing import procesar_video, procesar_imagen

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"

def main():
    picam2 = Picamera2()
 # Cambia al modo de enfoque manual
    picam2.set_controls({"AfMode": controls.AfModeEnum.Manual})

    # Configura la posición de la lente para enfocar a 30 cm
    lens_position = 1 / 0.3  # 1 / (distancia en metros)
    picam2.set_controls({"LensPosition": lens_position})
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (2000, 1125)}))
    picam2.start()

    try:
        # Procesa el video (en lugar de capturar y procesar una imagen)
        video_thread = threading.Thread(target=procesar_video, args=(picam2, sio))  # Cambio de socketio a sio
        video_thread.start()
        # Inicia el hilo de envío de estadísticas
        stats_thread = threading.Thread(target=enviar_estadisticas, args=(sio,))
        stats_thread.start()

        # Ejecuta la aplicación Flask en el hilo principal
        app.run(host="0.0.0.0", port=5000)

    finally:
        picam2.stop()

if __name__ == "__main__":
    main()
