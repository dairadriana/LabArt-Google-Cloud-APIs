import speech_recognition as sr

def reconocer_voz():
    reconocedor = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Ajustando al ruido ambiente. Por favor, mantén silencio.")
            reconocedor.adjust_for_ambient_noise(source, duration=2)
            print("Di algo:")
            audio = reconocedor.listen(source)

        try:
            texto = reconocedor.recognize_google(audio, language="es-ES")
            print("Texto reconocido: {}".format(texto))
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError as e:
            print("Error en la solicitud a Google Speech Recognition: {}".format(e))

if __name__ == "__main__":
    reconocer_voz()
