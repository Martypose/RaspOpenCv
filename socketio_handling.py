import socketio
import requests
cliente_conectado = False

# Crear una sesión de requests personalizada
http_session = requests.Session()
http_session.verify = './combined_certificates.pem'  # La ruta al archivo de certificados combinado

# Aumentar el tiempo de espera (timeout) para la conexión
http_session.timeout = 30  # Ajusta este valor según sea necesario


sio = socketio.Client(ssl_verify=False)

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

# Conectarse al servidor Socket.IO en el lado del servidor de Flask
sio.connect('https://www.maderaexteriores.com/api')

# Enviar un evento al servidor Socket.IO en el lado del servidor de Flask
enviar_evento('evento', {'mensaje': 'Hola desde Flask'})
