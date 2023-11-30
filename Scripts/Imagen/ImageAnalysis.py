import threading
import cv2
import os
import time
import tkinter as tk
from google.cloud import vision_v1
from google_images_search import GoogleImagesSearch
from PIL import Image, ImageTk
import requests
from io import BytesIO

square_size = 256

# Cliente de visión AI
client = vision_v1.ImageAnnotatorClient()

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
image_png_counter = 0
start_time = time.time()

# Configuración de la ventana de Tkinter
root = tk.Tk()
root.title("Webcam and Image Viewer")

# Configurar el tamaño de la ventana
root.geometry("1000x480")

# Crear un lienzo para mostrar la imagen y el video
canvas = tk.Canvas(root, width=1000, height=480)
canvas.pack()

def detect_labels(path):
    """Detects labels in the file."""
    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision_v1.Image(content=content)

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    query_Google = ' '.join(labels)
    print("Query: ", query_Google)

    retrieve_from_google(query_Google, 1)
    time.sleep(1)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

def retrieve_from_google(query, limit):
    folder_path = os.path.join(os.getcwd(), "Images")

    gis = GoogleImagesSearch('AIzaSyBm-zMIEyDd-9cyf3kzRbLCPdRit4hhjqs', 'd445dfdd970e94217')
    _search_params = {
        'q': query,
        'num': limit,
        'fileType': 'jpg|gif|png',
    }

    gis.search(search_params=_search_params, path_to_dir=folder_path)
    first_image_url = gis.results()[0].url

    # Mostrar la imagen de Google en el lienzo de Tkinter
    img_google = Image.open(BytesIO(requests.get(first_image_url).content))
    img_google = img_google.resize((500, 480))
    img_google_tk = ImageTk.PhotoImage(img_google)

    canvas.create_image(500, 0, anchor=tk.NW, image=img_google_tk)
    canvas.image = img_google_tk

def update_image():
    # Mostrar el frame de la webcam en el lienzo de Tkinter
    ret, frame = cam.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    img_tk = ImageTk.PhotoImage(img)

    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.img_tk = img_tk

def analyze_image():
    global image_png_counter
    global start_time

    img_name = "Test_Image_{}.png".format(image_png_counter)
    ret, frame = cam.read()
    cv2.imwrite(img_name, frame)
    threading.Thread(target=detect_labels, args=(img_name,)).start()
    os.remove(img_name)
    print("{} analyzed!".format(img_name))

    image_png_counter += 1
    start_time = time.time()

    # Programar la próxima ejecución del análisis después de un intervalo de tiempo
    root.after(5000, analyze_image)  # 5000 milisegundos = 5 segundos

# Iniciar el bucle de video
def video_loop():
    update_image()
    root.after(10, video_loop)

# Iniciar automáticamente el análisis después de un intervalo de tiempo
root.after(5000, analyze_image)  # Iniciar después de 5 segundos

# Iniciar el bucle principal de Tkinter
video_loop()
root.mainloop()

# Liberar la cámara al salir
cam.release()
cv2.destroyAllWindows()
