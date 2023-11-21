import pygame
import speech_recognition as sr

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ventana_ancho = 800
ventana_alto = 100
ventana = pygame.display.set_mode((ventana_ancho, ventana_alto))
pygame.display.set_caption("Texto Reconocido")

# Configuración de texto
fuente = pygame.font.Font(None, 36)
color_texto = (255, 255, 255)

def mostrar_texto(texto):
    texto_superficie = fuente.render(texto, True, color_texto)
    ventana.blit(texto_superficie, (ventana_ancho, ventana_alto // 2))
    pygame.display.flip()

def reconocer_voz():
    reconocedor = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Ajustando al ruido ambiente. Por favor, mantén silencio.")
            reconocedor.adjust_for_ambient_noise(source, duration=5)
            print("Di algo:")
            audio = reconocedor.listen(source)

        try:
            texto = reconocedor.recognize_google(audio, language="es-ES")
            print("Texto reconocido: {}".format(texto))
            mostrar_texto(texto)
            pygame.time.delay(100)  # Pequeño retraso para ver el texto
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError as e:
            print("Error en la solicitud a Google Speech Recognition: {}".format(e))

if __name__ == "__main__":
    reconocer_voz()
