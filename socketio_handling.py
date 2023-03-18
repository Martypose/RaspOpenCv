# socketio_handling.py
import socketio
import certifi
cliente_conectado = False

sio = socketio.Client()

@sio.event
def connect():
    global cliente_conectado
    cliente_conectado = True
    print("Client connected")

@sio.event
def disconnect():
    global cliente_conectado
    cliente_conectado = False
    print("Client disconnected")
    
def esta_conectado():  # Función para devolver el estado de cliente_conectado
    global cliente_conectado
    return cliente_conectado

# Función para enviar un evento
def enviar_evento(nombre_evento, datos):
    sio.emit(nombre_evento, datos)
#
# Conectarse al servidor Socket.IO en el lado del servidor de Flask
sio.connect('https://www.maderaexteriores.com:3001')

# Enviar un evento al servidor Socket.IO en el lado del servidor de Flask
enviar_evento('evento', {'mensaje': 'Hola desde Flask'})