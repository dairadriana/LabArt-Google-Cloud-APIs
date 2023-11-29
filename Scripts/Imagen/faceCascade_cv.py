import cv2
import threading
import time
from deepface import DeepFace

# Configuración de la webcam
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Ancho del frame
cam.set(4, 480)  # Altura del frame

# Cargar el clasificador preentrenado para la detección de caras
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Crear una ventana llamada 'Video en tiempo real'
cv2.namedWindow('Video en tiempo real', cv2.WINDOW_NORMAL)

# Nombre fijo para la captura de pantalla
screenshot_filename = "captura_screenshot.png"

# Bandera para controlar la toma de capturas de pantalla
capture_flag = False

# Variables para la detección de emociones en un hilo separado
emotion_detected = False
emotion_result = None

# Función para la captura de pantalla en un hilo separado
def capture_screenshot():
    global capture_flag

    while True:
        if capture_flag:
            # Capturar un frame desde la webcam
            ret, frame = cam.read()

            # Guardar la captura de pantalla (sobrescribiendo la anterior)
            cv2.imwrite(screenshot_filename, frame)

            # Indicar que se ha tomado la captura
            global emotion_detected
            emotion_detected = True

            capture_flag = False

# Función para la detección de emociones en un hilo separado
def detect_emotion():
    global emotion_detected, emotion_result

    while True:
        if emotion_detected:
            # Cargar la imagen desde el archivo
            image = cv2.imread(screenshot_filename)

            # Verificar si la imagen se cargó correctamente
            if image is not None:
                # Intentar detectar rostros en la imagen
                faces = face_cascade.detectMultiScale(image, scaleFactor=1.3, minNeighbors=5)

                # Verificar si se detectó al menos un rostro
                if len(faces) > 0:
                    # Realizar la clasificación de emociones
                    result = DeepFace.analyze(image, actions=['emotion'])

                    # Acceder a la acción 'emotion' directamente
                    emotion_result = result[0]['emotion'] if len(result) > 0 else None
                else:
                    emotion_result = None
            else:
                print("Error al cargar la imagen.")

            emotion_detected = False

# Iniciar las funciones en hilos separados
capture_thread = threading.Thread(target=capture_screenshot)
capture_thread.start()

emotion_thread = threading.Thread(target=detect_emotion)
emotion_thread.start()

# Bucle principal para capturar y mostrar el video en tiempo real
while True:
    # Capturar un frame desde la webcam
    ret, frame = cam.read()

    # Convertir el frame a escala de grises para la detección de caras
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar caras en el frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Dibujar un rectángulo verde y agregar la emoción debajo de cada rostro detectado
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Verificar si hay una emoción detectada
        if emotion_result is not None:
            # Agregar la emoción debajo del cuadrado verde
            text = f"Emoción: {emotion_result['emotion']}" if 'emotion' in emotion_result else "No se detectó emocion"
            cv2.putText(frame, text, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Mostrar el frame con los rectángulos y texto en la ventana
    cv2.imshow('Video en tiempo real', frame)

    # Tomar una captura de pantalla cada 5 segundos
    if int(time.time()) % 5 == 0:
        capture_flag = True

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la webcam y cerrar la ventana al salir
cam.release()
cv2.destroyAllWindows()
