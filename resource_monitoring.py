import psutil
import time

def enviar_estadisticas(socketio):
    while True:
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        stats = {"cpu_percent": cpu_percent, "memory_percent": memory}
        print("Enviando estadísticas al servidor nodejs")
        socketio.emit("estadisticas", stats)
        time.sleep(10)
        
