import pygame
import speech_recognition as sr
import sys

# Inicializar Pygame
pygame.init()

def mostrar_texto_ventana(texto):
    # Configuración de la nueva ventana
    ventana_ancho = 800
    ventana_alto = 100
    nueva_ventana = pygame.display.set_mode((ventana_ancho, ventana_alto))
    pygame.display.set_caption("Texto Reconocido")

    # Configuración de texto
    fuente = pygame.font.Font(None, 36)
    color_texto = (255, 255, 255)

    ejecutando = True
    clock = pygame.time.Clock()

    while ejecutando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
                pygame.quit()
                sys.exit()

        nueva_ventana.fill((0, 0, 0))  # Limpiar la pantalla en cada iteración
        texto_superficie = fuente.render(texto, True, color_texto)
        nueva_ventana.blit(texto_superficie, (ventana_ancho // 2 - texto_superficie.get_width() // 2, ventana_alto // 2))
        pygame.display.flip()

        clock.tick(30)  # Limitar la velocidad de actualización a 30 FPS

    pygame.quit()

def reconocer_voz():
    reconocedor = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Ajustando al ruido ambiente. Por favor, mantén silencio.")
                reconocedor.adjust_for_ambient_noise(source, duration=1)
                print("Di algo:")
                audio = reconocedor.listen(source)

            texto = reconocedor.recognize_google(audio, language="es-ES")
            print("Texto reconocido: {}".format(texto))
            mostrar_texto_ventana(texto)
            pygame.time.delay(50)  # Reducción del retraso para mostrar más rápido
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError as e:
            print("Error en la solicitud a Google Speech Recognition: {}".format(e))
        except KeyboardInterrupt:
            # Manejar la interrupción de teclado (por ejemplo, Ctrl+C para detener el programa)
            break

if __name__ == "__main__":
    try:
        reconocer_voz()
    except Exception as e:
        print("Error inesperado: {}".format(e))
    finally:
        pygame.quit()
