from google.cloud import speech_v1p1beta1 as speech
import os

# Establece la variable de entorno GOOGLE_APPLICATION_CREDENTIALS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\tokyo\Desktop\Programming\Incubadora de Arte y Tec\incubadora-arte-y-tec-e0a1f15abd62.json"

def transcribe_speech(audio_file_path):
    client = speech.SpeechClient()

    with open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,  # Deja que la API detecte automáticamente la codificación
        sample_rate_hertz=16000,  # Ajusta la frecuencia de muestreo según tu archivo
        language_code="es-ES",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcripción: {}".format(result.alternatives[0].transcript))

if __name__ == "__main__":
    audio_file_path = r"C:\Users\tokyo\Desktop\Programming\Incubadora de Arte y Tec\Audios\MasAllaDelRosa_1.mp3"
    transcribe_speech(audio_file_path)
