# RaspOpenCv

Este proyecto utiliza Python Flask, OpenCV y Socket.IO para crear una aplicación que realiza el monitoreo y procesamiento en tiempo real de imágenes de una cámara convencional. La aplicación detecta tablas que salen de un aserradero, calcula sus medidas y envía la información a través de Socket.IO para su visualización y análisis en tiempo real.

## Características

- Captura de imágenes en tiempo real desde una cámara convencional
- Procesamiento de imágenes utilizando OpenCV para detectar tablas en el aserradero
- Cálculo de medidas de las tablas detectadas
- Envío de medidas y estadísticas de recursos del sistema a través de Socket.IO

## Instalación y configuración

1. Clone este repositorio en su máquina local
2. Asegúrese de tener Python 3.x instalado y cree un entorno virtual con Conda
3. Ejecute la aplicación con `python app.py`

## Estructura del proyecto

- `app.py`: Archivo principal de la aplicación Flask y punto de entrada
- `routes.py`: Define las rutas y funciones asociadas de la aplicación Flask
- `socketio_handling.py`: Funciones para manejar eventos de conexión y desconexión de Socket.IO y envío de datos
- `video_processing.py`: Funciones para procesar imágenes capturadas y detectar tablas
- `resource_monitoring.py`: Funciones para monitorear los recursos del sistema y enviar estadísticas a través de Socket.IO
