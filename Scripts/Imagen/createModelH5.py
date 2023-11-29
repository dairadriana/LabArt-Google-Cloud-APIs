import pandas as pd
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical

# Cargar el conjunto de datos FER2013 desde el archivo CSV
fer2013_df = pd.read_csv('C:\\Users\\tokyo\\Desktop\\Programming\\LabArt-Google-Cloud-APIs\\Scripts\\Imagen\\fer2013.csv')

# Extraer las imágenes y las etiquetas del conjunto de datos
images = []
labels = fer2013_df['emotion']

for pixel_sequence in fer2013_df['pixels']:
    image = [int(pixel) for pixel in pixel_sequence.split(' ')]
    images.append(np.array(image, dtype=np.uint8).reshape((48, 48, 1)))

images = np.array(images) / 255.0
labels = np.array(labels)

# Convertir etiquetas a formato one-hot
le = LabelEncoder()
labels = to_categorical(le.fit_transform(labels))

# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Definir la arquitectura del modelo
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(7, activation='softmax'))  # 7 clases de emociones

# Compilar el modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_test, y_test))

# Guardar el modelo en formato h5
model.save('modelo_emociones.h5')
