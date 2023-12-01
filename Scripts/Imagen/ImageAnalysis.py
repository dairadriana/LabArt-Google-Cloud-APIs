import threading
import cv2
import os
import time
import tkinter as tk
from google.cloud import vision_v1
from google_images_search import GoogleImagesSearch
from PIL import Image, ImageTk
import requests
import random

# Configuración de la ventana de Tkinter
root = tk.Tk()
root.title("Webcam and Image Viewer")

# Tamaño de la ventana
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Cliente de visión AI
client = vision_v1.ImageAnnotatorClient()

image_list = []

# Calcular la posición vertical para centrar la webcam
vertical_position = (screen_height - (screen_height // 2)) // 2

# Crear una cámara con el nuevo tamaño
cam = cv2.VideoCapture(0)
new_width = screen_width // 2  # ajusta según tus necesidades
new_height = screen_height // 2  # ajusta según tus necesidades
cam.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)
cam.set(2, vertical_position)  # Posición vertical centrada

# Configurar el tamaño de la ventana principal
root.geometry(f"{screen_width}x{screen_height}")

# Crear un lienzo para mostrar la imagen y el video
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack()

# Crear una nueva ventana para mostrar las queries
query_window = tk.Toplevel(root)
query_window.title("Queries")

# Configurar la ventana de queries para ocupar toda la pantalla
query_window.attributes('-fullscreen', True)

# Configurar el fondo negro del widget de texto
query_text = tk.Text(query_window, wrap=tk.WORD, width=screen_width, height=screen_height, bg='black', fg='green', font=('Arial', 14))
query_text.pack()

def add_neon_border(image_path):
    img = Image.open(image_path)
    
    # Configurar el color del borde (en este caso, verde neón)
    border_color = (0, 255, 0)  # R, G, B
    
    # Tamaño del borde
    border_size = 10
    
    # Crear una nueva imagen con el borde
    bordered_img = Image.new("RGB", (img.width + 2 * border_size, img.height + 2 * border_size), border_color)
    
    # Pegar la imagen original en el centro de la nueva imagen
    bordered_img.paste(img, (border_size, border_size))
    
    return bordered_img


def clear_images(folder_path, max_images=250):
    # Obtener la lista de todas las imágenes en el directorio
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Ordenar las imágenes por fecha de creación (más antigua primero)
    image_files.sort(key=lambda x: os.path.getctime(os.path.join(folder_path, x)))

    # Eliminar imágenes antiguas si hay más de max_images
    if len(image_files) > max_images:
        images_to_delete = len(image_files) - max_images
        for i in range(images_to_delete):
            file_path = os.path.join(folder_path, image_files[i])
            try:
                os.remove(file_path)
                print(f"Imagen eliminada: {file_path}")
            except Exception as e:
                print(f"Error al eliminar {file_path}: {e}")

def detect_labels(path):
    """Detects labels in the file."""
    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision_v1.Image(content=content)

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    query_Google = ' '.join(labels)
    print("Query: ", query_Google)

    # Mostrar la query en la ventana de texto
    query_text.insert(tk.END, f"{query_Google}\n")

    retrieve_from_google(query_Google, 10)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

def retrieve_from_google(query, limit):
    folder_path = os.path.join(os.getcwd(), "Images")

    # Limpiar imágenes antiguas
    clear_images(folder_path, max_images=250)

    gis = GoogleImagesSearch('AIzaSyBm-zMIEyDd-9cyf3kzRbLCPdRit4hhjqs', 'd445dfdd970e94217')

    _search_params = {
        'q': query,
        'num': limit,
        'fileType': 'jpg|gif|png',
    }

    gis.search(search_params=_search_params, path_to_dir=folder_path)

    # Obtener 2 resultados aleatorios
    random_indices = random.sample(range(limit), 3)
    image_urls = [gis.results()[i].url for i in random_indices]

    for i, image_url in enumerate(image_urls):
        # Generar un nombre único para cada imagen
        image_name = f"image_{i}.jpg"
        image_path = os.path.join(folder_path, image_name)

        # Guardar la imagen en la carpeta
        with open(image_path, 'wb') as f:
            f.write(requests.get(image_url).content)

        # Abrir la imagen con Pillow (PIL)
        img_pil = Image.open(image_path)

        # Calcular el nuevo ancho manteniendo la relación de aspecto original
        ratio = 250 / float(img_pil.size[1])
        new_width = int(float(img_pil.size[0]) * float(ratio))
        new_height = int(float(img_pil.size[1]) * float(ratio))

        # Redimensionar la imagen
        img_pil = img_pil.resize((new_width, 250), Image.BILINEAR)

        # Calcular posición aleatoria en el lienzo
        img_width = screen_width // 2
        img_height = screen_height
        img_x = random.randint(0, screen_width - new_width)
        img_y = random.randint(0, screen_height - new_height)

        # Mostrar la imagen en el lienzo de Tkinter
        img_google = Image.open(image_path)
        img_google = img_google.resize((img_width, img_height))
        img_google_tk = ImageTk.PhotoImage(img_pil)

        canvas.create_image(img_x, img_y, anchor=tk.NW, image=img_google_tk)
        canvas.image = img_google_tk
        root.update()

        # Agregar la imagen a la lista
        image_list.append((img_google_tk, img_x, img_y))

# Modificación en la función update_image para centrar la webcam en su espacio designado
def update_image():
    # Mostrar el frame de la webcam en el lienzo de Tkinter
    ret, frame = cam.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Calcular el tamaño y la posición para centrar la webcam en su espacio designado
    img_width = new_width
    img_height = new_height
    img_x = 0  # Izquierda
    img_y = 0

    img = Image.fromarray(cv2image)
    img = img.resize((img_width, img_height))  # Ajustar el tamaño de la imagen sin antialiasing
    img_tk = ImageTk.PhotoImage(img)

    canvas.create_image(img_x, img_y, anchor=tk.NW, image=img_tk)
    canvas.img_tk = img_tk

def analyze_image():
    global start_time

    img_name = "Test_Image.png"
    ret, frame = cam.read()
    cv2.imwrite(img_name, frame)
    threading.Thread(target=detect_labels, args=(img_name,)).start()
    print("{} analyzed!".format(img_name))
    start_time = time.time()

    # Programar la próxima ejecución del análisis después de un intervalo de tiempo
    root.after(3000, analyze_image)  # 5000 milisegundos = 5 segundos

# Iniciar el bucle de video
def video_loop():
    update_image()
    root.after(10, video_loop)

# Iniciar automáticamente el análisis después de un intervalo de tiempo
root.after(10, analyze_image)  # Iniciar después de 5 segundos

# Iniciar el bucle principal de Tkinter
video_loop()
root.mainloop()

# Liberar la cámara al salir
cam.release()
cv2.destroyAllWindows()