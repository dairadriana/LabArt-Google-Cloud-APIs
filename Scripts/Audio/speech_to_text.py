import os
import io
import pyaudio
import wave
from google.cloud import speech_v1p1beta1 as speech
import os

# Establece la variable de entorno GOOGLE_APPLICATION_CREDENTIALS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\tokyo\Desktop\Programming\Incubadora de Arte y Tec\incubadora-arte-y-tec-e0a1f15abd62.json"

def main():
    # Configura la conexión al servicio de Speech-to-Text
    client = speech.SpeechClient()
    
    # Configura la captura de audio desde el micrófono
    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)

    print("Habla y presiona Ctrl+C para detener la grabación...")

    try:
        while True:
            audio_data = stream.read(1024)
            response = client.recognize(
                config={
                    "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
                    "sample_rate_hertz": 16000,
                    "language_code": "es-ES",
                },
                audio={"content": audio_data},
            )
            for result in response.results:
                print("Transcripción en tiempo real: {}".format(result.alternatives[0].transcript))
    except KeyboardInterrupt:
        pass
    finally:
        print("Deteniendo la grabación...")
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()