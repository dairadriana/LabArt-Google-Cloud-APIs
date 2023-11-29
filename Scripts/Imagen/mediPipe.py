import cv2
import mediapipe as mp

# Inicializar el módulo Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Configurar la cámara
cap = cv2.VideoCapture(0)
width, height = 640, 480
cap.set(3, width)
cap.set(4, height)

# Inicializar variables
likes_count = 0
threshold = 0.9  # Umbral de confianza para considerar que el pulgar está levantado

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir la imagen a RGB para el módulo Mediapipe Hands
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Obtener los resultados de la detección de manos
    results = hands.process(rgb_frame)

    # Verificar si se detectó alguna mano
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Obtener la posición del pulgar
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_tip_x, thumb_tip_y = int(thumb_tip.x * width), int(thumb_tip.y * height)

            # Dibujar un círculo en la posición del pulgar
            cv2.circle(frame, (thumb_tip_x, thumb_tip_y), 10, (0, 255, 0), -1)

            # Verificar si el pulgar está levantado (basado en la posición y el umbral de confianza)
            if thumb_tip_y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height and \
                    results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_TIP].visibility > threshold:
                # Incrementar el contador de likes
                likes_count += 1
                print(f"Likes: {likes_count}")

    # Mostrar el resultado
    cv2.imshow('Thumb Up Counter', frame)

    # Salir del bucle cuando se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
