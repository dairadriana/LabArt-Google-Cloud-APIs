import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

# Cargar el modelo preentrenado
model = load_model('C:\\Users\\tokyo\\Desktop\\Programming\\LabArt-Google-Cloud-APIs\\modelo_emociones.h5')

# Crear una lista de emociones
emotions = ["Enojo", "Asco", "Miedo", "Feliz", "Neutral", "Triste", "Sorpresa"]

# Iniciar el clasificador de caras de OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Iniciar la captura de la cámara web
cap = cv2.VideoCapture(0)

while True:
    # Capturar un frame
    ret, frame = cap.read()

    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar caras en la imagen
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Extraer la región de interés (ROI) correspondiente a la cara detectada
        roi = gray[y:y + h, x:x + w]

        # Redimensionar la imagen a las dimensiones esperadas por el modelo
        roi = cv2.resize(roi, (48, 48))

        # Normalizar la imagen
        roi = roi / 255.0

        # Expandir las dimensiones para que coincidan con las dimensiones de entrada del modelo
        roi = np.expand_dims(roi, axis=0)
        roi = np.expand_dims(roi, axis=-1)

        # Hacer la predicción
        prediction = model.predict(roi)[0]

        # Obtener la emoción predicha
        predicted_emotion = emotions[np.argmax(prediction)]

        # Dibujar un cuadrado morado alrededor del rostro detectado
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)

        # Mostrar la emoción predicha en el frame
        cv2.putText(frame, predicted_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

    # Mostrar el frame
    cv2.imshow('Emotion Detection', frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
