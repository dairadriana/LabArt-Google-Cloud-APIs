import cv2
from google.cloud import vision

def detect_faces_emotions(frame):
    client = vision.ImageAnnotatorClient()

    # Convierte el frame en un formato que Cloud Vision pueda entender
    _, img_encoded = cv2.imencode(".jpg", frame)
    image = vision.Image(content=img_encoded.tostring())

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )

    for face in faces:
        vertices = [((vertex.x, vertex.y)) for vertex in face.bounding_poly.vertices]

        # Dibuja un rectángulo alrededor de la cara
        for i in range(3):
            cv2.line(frame, vertices[i], vertices[i + 1], (0, 255, 0), 2)
        cv2.line(frame, vertices[3], vertices[0], (0, 255, 0), 2)

        # Muestra la etiqueta de emoción más probable en la parte superior del rectángulo
        max_emotion = max(
            ["anger", "joy", "surprise", "sorrow"],
            key=lambda emotion: getattr(face, f"{emotion}_likelihood"),
        )
        emotion_label = f"{max_emotion.capitalize()}: {likelihood_name[getattr(face, f'{max_emotion}_likelihood')]}"

        cv2.putText(frame, emotion_label, (vertices[0][0], vertices[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

    return frame

def draw_faces_emotions_realtime():
    # Inicializa la webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Llama a la función detect_faces para detectar caras en el frame
        frame_with_faces = detect_faces_emotions(frame)

        # Muestra el frame con las caras y emociones detectadas
        cv2.imshow("Webcam", frame_with_faces)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Libera la cámara y cierra todas las ventanas
    cap.release()
    cv2.destroyAllWindows()
