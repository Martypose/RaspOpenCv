# socketio_handling.py
import socketio

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

sio.connect('https://www.maderaexteriores.com/api/')