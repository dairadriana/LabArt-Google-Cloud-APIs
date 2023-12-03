import threading
import cv2
import os
import time
from unidecode import unidecode
import tkinter as tk
from google.cloud import vision_v1
from google_images_search import GoogleImagesSearch
from PIL import Image, ImageTk
import requests
from screeninfo import get_monitors
import random

# Configuración de la ventana de Tkinter
root = tk.Tk()
root.title("Image Viewer")

# Obtener información sobre los monitores
monitors = get_monitors()

# Tamaño de la ventana
screen_width = monitors[0].width
screen_height = monitors[0].height

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

root.geometry(f"{monitors[0].width}x{monitors[0].height}+0+0")

# Crear un lienzo para mostrar la imagen y el video
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack()

# Crear una nueva ventana para mostrar las queries
query_window = tk.Toplevel(root)
query_window.title("Queries")

# Configurar el fondo negro del widget de texto
query_text = tk.Text(query_window, wrap=tk.WORD, width=screen_width, height=screen_height, bg='black', fg='green', font=('Arial', 14))

query_text.tag_configure("labels_tag", foreground="green")
query_text.tag_configure("text_tag", foreground="blue")
query_text.tag_configure("logos_tag", foreground="pink")

query_text.pack()

query_window.geometry(f"{monitors[1].width}x{monitors[1].height}+{monitors[1].x}+{monitors[1].y}")


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

def detect_text(path):

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision_v1.Image(content=content)

    response_text = client.text_detection(image=image)
    texts = [unidecode(text.description) for text in response_text.text_annotations]

    # Verificar si hay texto antes de imprimir el mensaje
    if texts:
        query_text.insert(tk.END, f"{texts}\n", "text_tag")
        query_text.update_idletasks()  # Actualizar tareas pendientes
        query_text.yview(tk.END)
        query_Google_text = ' '.join(texts)

        retrieve_from_google(query_Google_text, 10)

    if response_text.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response_text.error.message)
        )

def detect_labels_logos(path):
    
    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision_v1.Image(content=content)

    response_labels = client.label_detection(image=image)
    labels = [label.description for label in response_labels.label_annotations]

    # Detectar logos
    response_logos = client.logo_detection(image=image)
    logos = [logo.description for logo in response_logos.logo_annotations]

    # Verificar si hay logos antes de imprimir el mensaje
    if logos:
        # Mostrar la query en la ventana de texto
        query_text.insert(tk.END, f"{logos}\n", "logos_tag")
        query_text.update_idletasks()  # Actualizar tareas pendientes
        query_text.yview(tk.END)

    # Combinar descripciones de labels y logos
    query_Google_labels = ' '.join(labels)
    query_Google_logos = ' '.join(logos) if logos else ''
    query_Google_combined = f"{query_Google_labels} {query_Google_logos}"

    # Mostrar la query en la ventana de texto
    query_text.insert(tk.END, f"{query_Google_combined}\n", "labels_tag")

    retrieve_from_google(query_Google_combined, 10)

    if response_labels.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response_labels.error.message)
        )
    if response_logos.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response_logos.error.message)
        )
    
def add_browser_frame(img, frame_path='C:\\Users\\tokyo\\Desktop\\Programming\\LabArt-Google-Cloud-APIs\\Scripts\\Imagen\\browser_frame.png', border_height=35, image_offset=2):
    # Abrir el marco del navegador
    frame = Image.open(frame_path)

    # Ajustar el tamaño del marco para que sea más alto que la imagen
    frame = frame.resize((img.width + 5, img.height + border_height))

    # Calcular la posición horizontal para centrar la imagen
    horizontal_position = (frame.width - img.width) // 2

    # Combinar la imagen original con el marco, posicionando la imagen 2 píxeles arriba del límite inferior
    img_with_frame = Image.alpha_composite(Image.new("RGBA", frame.size, (255, 255, 255, 255)), frame)
    img_with_frame.paste(img, (horizontal_position, border_height - image_offset))

    # Convertir a formato RGB si no está en ese formato
    img_with_frame = img_with_frame.convert('RGB')

    return img_with_frame

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

        # Agregar el borde al estilo de la ventana del navegador
        img_with_frame = add_browser_frame(img_pil)

        # Calcular posición aleatoria en el lienzo
        img_x = random.randint(0, screen_width - new_width)
        img_y = random.randint(0, screen_height - 250)  # Usar 250 para la altura con el borde

        # Mostrar la imagen en el lienzo de Tkinter
        img_google_tk = ImageTk.PhotoImage(img_with_frame)

        canvas.create_image(img_x, img_y, anchor=tk.NW, image=img_google_tk)
        canvas.image = img_google_tk
        root.update()

        # Agregar la imagen a la lista
        image_list.append((img_google_tk, img_x, img_y))

def analyze_image():
    global start_time

    img_name = "Test_Image.png"
    ret, frame = cam.read()
    cv2.imwrite(img_name, frame)

    threading.Thread(target=detect_labels_logos, args=(img_name,)).start()
    threading.Thread(target=detect_text, args=(img_name,)).start()

    print("{} analyzed!".format(img_name))
    start_time = time.time()

    # Programar la próxima ejecución del análisis después de un intervalo de tiempo
    root.after(3000, analyze_image)  # 5000 milisegundos = 5 segundos

# Iniciar el bucle de video
def video_loop():
    #update_image()
    root.after(10, video_loop)

def exit_program(event):
    root.destroy()  # Cierra la ventana principal de Tkinter, lo que terminará el programa

# Asociar la pulsación de la tecla "q" con la función exit_program
root.bind('<KeyPress-q>', exit_program)

def on_closing():
    cam.release()
    cv2.destroyAllWindows()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar automáticamente el análisis después de un intervalo de tiempo
root.after(10, analyze_image)  # Iniciar después de 5 segundos

# Iniciar el bucle principal de Tkinter
video_loop()
root.mainloop()
