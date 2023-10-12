import openai
import cv2
import os
import time
import urllib.request
from PIL import Image
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from vision_detect_labels import detect_labels
from vision_detect_colors import detect_properties
from vision_detect_faces import detect_faces
from vision_detect_logos import detect_logos
from face_detection import detect_face_in_realtime

square_size = 256

# Cliente de visión AI
client = vision_v1.ImageAnnotatorClient()

# API de OpenAI - DALL-E
api_key = "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"
openai.api_key = api_key

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
image_counter = 0
image_png_counter = 0
frame_set = []
start_time = time.time()

detect_face_in_realtime()

# Cambiar a while true para hacer el ciclo bucle
while image_png_counter < 1:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if time.time() - start_time >= 5: #<---- cada 5 segundos
        img_name = "Test_Image_{}.png".format(image_png_counter)
        cv2.imwrite(img_name, frame)
        #detect_properties(img_name)
        #detect_labels(img_name)
        detect_faces(img_name)

        # Cortar la imagen en formato cuadrado
        #im = Image.open('Test_Image_{}.png'.format(image_png_counter))
        #left = int(im.size[0] / 2 - square_size / 2)
        #upper = int(im.size[1] / 2 - square_size / 2)
        #right = left + square_size
        #lower = upper + square_size
        #im_cropped = im.crop((left, upper,right,lower))
        #im_cropped.save('Test_Image_Square_{}.png'.format(image_png_counter))
        
        # os.remove('Test_Image_{}.png'.format(image_png_counter))

        # print("{} written!".format(image_png_counter))
        image_png_counter += 1
        start_time = time.time()
    image_counter += 1


# Quitar comentario para correr en API
# response = openai.Image.create_variation(
#    image = open("Test_Image_Square_0.png", "rb"),
#    n=1,
#    size="256x256"
#)
#url = response["data"][0]["url"]
#urllib.request.urlretrieve(url, "Test_Image_Square_0_API.png")
#img = Image.open(r"Test_Image_Square_0_API.png")
#img.save('API_Result.png')