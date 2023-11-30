import threading
import cv2
import os
import time
from google.cloud import vision_v1
from vision_detect_labels import detect_labels
from vision_detect_logos import detect_logos

square_size = 256

# Cliente de visión AI
client = vision_v1.ImageAnnotatorClient()

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
image_counter = 0
image_png_counter = 0
frame_set = []
start_time = time.time()

def analyze_image(frame):
    img_name = "Test_Image_{}.png".format(image_png_counter)
    cv2.imwrite(img_name, frame)
    detect_labels(img_name)
    os.remove(img_name)
    print("{} analyzed!".format(img_name))

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if time.time() - start_time >= 5:  # cada 5 segundos
        # Iniciar un hilo para el análisis de la imagen
        threading.Thread(target=analyze_image, args=(frame.copy(),)).start()

        image_png_counter += 1
        start_time = time.time()

    image_counter += 1

# Liberar la cámara y cerrar la ventana al salir
cam.release()
cv2.destroyAllWindows()
