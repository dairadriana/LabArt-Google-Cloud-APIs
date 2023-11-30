import cv2
import numpy as np
import threading
import time
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import speech_recognition as sr

# Load the pretrained model
model = load_model('C:\\Users\\tokyo\\Desktop\\Programming\\LabArt-Google-Cloud-APIs\\modelo_emociones.h5')

# Create a list of emotions
emotions = ["ANGRY", "DISGUST", "FEAR", "HAPPY", "NEUTRAL", "SAD", "SURPRISE"]

# Initialize the OpenCV face classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the webcam capture
cap = cv2.VideoCapture(0)

# Initialize the SpeechRecognition recognizer
recognizer = sr.Recognizer()

# Variable para almacenar el texto reconocido
recognized_text = ""

# Set the font and color
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
color = (0, 204, 0)  # White color in RGB

# Función para realizar el reconocimiento de emociones
def recognize_emotion(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Extract the region of interest (ROI) corresponding to the detected face
        roi = gray[y:y + h, x:x + w]

        # Resize the image to the dimensions expected by the model
        roi = cv2.resize(roi, (48, 48))

        # Normalize the image
        roi = roi / 255.0

        # Expand dimensions to match the input dimensions of the model
        roi = np.expand_dims(roi, axis=0)
        roi = np.expand_dims(roi, axis=-1)

        # Make the prediction
        prediction = model.predict(roi)[0]

        # Get the predicted emotion
        predicted_emotion = emotions[np.argmax(prediction)]

        # Draw a purple rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)

        # Display the detected emotion with customized text settings
        cv2.putText(frame, f"Emotion detected: {predicted_emotion}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

# Función para realizar la transcripción de audio
def transcribe_audio():
    global recognized_text

    while True:
        # Use SpeechRecognition to perform speech-to-text in English and Spanish
        with sr.Microphone() as source:
            try:
                audio_data = recognizer.listen(source, timeout=5)
                recognized_text = recognizer.recognize_google(audio_data, language=['en-US', 'es-ES'])
            except sr.UnknownValueError:
                pass  # Ignore if no speech is detected
            except sr.RequestError as e:
                print(f"Error with the speech recognition service; {e}")

# Iniciar el hilo para la transcripción de audio
audio_thread = threading.Thread(target=transcribe_audio)
audio_thread.start()

while True:
    # Capture a frame
    ret, frame = cap.read()

    # Verify if the frame was captured successfully
    if not ret:
        print("Error capturing the frame.")
        break

    # Realizar el reconocimiento de emociones en un hilo separado
    emotion_thread = threading.Thread(target=recognize_emotion, args=(frame,))
    emotion_thread.start()

    # Mostrar el texto reconocido en la pantalla
    cv2.putText(frame, f"Speech: {recognized_text}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Esperar a que el hilo de emociones termine antes de mostrar el siguiente frame
    emotion_thread.join()

    # Show the frame
    cv2.imshow('Emotion Detection', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()