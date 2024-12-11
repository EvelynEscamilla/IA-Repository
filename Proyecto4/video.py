import yt_dlp
import whisper
import os

def descargar_audio_youtube(url_video, archivo_audio="audio.webm"):
    # Descargar el audio del video de YouTube usando yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',  # Descargar solo el audio en la mejor calidad
        'outtmpl': archivo_audio,    # Guardar como archivo temporal
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url_video])  # Descargar el audio

def transcribir_audio(archivo_audio):
    # Cargar el modelo de Whisper
    model = whisper.load_model("base")

    # Transcribir el audio
    result = model.transcribe(archivo_audio)

    return result['text']

def main():
    # URL del video de YouTube que deseas transcribir
    url_video = input("Introduce la URL del video de YouTube: ")

    # Descargar el audio del video
    print("Descargando el audio del video...")
    descargar_audio_youtube(url_video)

    # Transcribir el audio descargado
    print("Transcribiendo el audio...")
    texto_transcrito = transcribir_audio("audio.webm")  # Usamos el formato descargado (webm o m4a)
    
    # Mostrar la transcripción
    print("\nTranscripción del video:\n")
    print(texto_transcrito)

    # Eliminar el archivo de audio después de la transcripción
    os.remove("audio.webm")

if __name__ == "__main__":
    main()
