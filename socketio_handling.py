cliente_conectado = False


def handle_connect():
    global cliente_conectado
    cliente_conectado = True
    print("Client connected")

def handle_disconnect():
    global cliente_conectado
    cliente_conectado = False
    print("Client disconnected")
    
def esta_conectado():  # Función para devolver el estado de cliente_conectado
    global cliente_conectado
    return cliente_conectado