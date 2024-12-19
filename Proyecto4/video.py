from pydub import AudioSegment
import os

def convert_video_to_audio(video_path: str, output_path: str):
    try:
        print("Convirtiendo video a MP3...")

        if not os.path.exists(video_path):
            print("El archivo de video no existe.")
            return

        audio = AudioSegment.from_file(video_path, format="mp4")
        
        mp3_file = os.path.join(output_path, "audio.mp3")
        audio.export(mp3_file, format="mp3")
        
        print(f"Audio extraído y guardado como {mp3_file}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    video_path = "C:/Users/ShiEu/Downloads/Estos son los puntos más importantes de la Reforma Judicial - Despierta.mp4"  
    output_path = "." 
    convert_video_to_audio(video_path, output_path)
