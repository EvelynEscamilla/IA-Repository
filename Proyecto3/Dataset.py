import os
import cv2
import yt_dlp as ytdlp # type: ignore

def generar_dataset(video_url, output_folder, resolution=(80, 80)):
    # Crear carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Usar yt-dlp para obtener el flujo de video
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'temp_video.%(ext)s',
        'noplaylist': True,
        'quiet': True,
    }

    with ytdlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        video_url = info_dict.get('url', None)
        print(f"Usando URL: {video_url}")

    # Abrir el video
    cap = cv2.VideoCapture(video_url)
    frame_count = 0
    img_count = 0

    while True:
        # Leer el siguiente frame del video
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir el frame a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Recortar y guardar las imágenes
        img_resized = cv2.resize(frame, resolution)
        cv2.imwrite(f"{output_folder}/frame_{img_count}.jpg", img_resized)
        img_count += 1

        frame_count += 1
        print(f"Procesando frame {frame_count}...")

    cap.release()
    print(f"Dataset generado en {output_folder}")

# Llamada a la función
video_url = "https://www.youtube.com/watch?v=EwXCyZffCTg"  # Enlace de video
output_folder = "C:/Users/ShiEu/Documents/dataset_coches"
generar_dataset(video_url, output_folder)
