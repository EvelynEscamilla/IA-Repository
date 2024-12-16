import os
import cv2
import numpy as np

def ajustar_brillo_contraste(frame, alpha=1.0, beta=0):
    return cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

def recortar_aleatoriamente(frame, porcentaje=0.1):
    h, w = frame.shape[:2]
    dy, dx = int(h * porcentaje), int(w * porcentaje)
    x1, y1 = np.random.randint(0, dx), np.random.randint(0, dy)
    return frame[y1:h - dy + y1, x1:w - dx + x1]

def aplicar_zoom(frame, factor=1.2):
    h, w = frame.shape[:2]
    nh, nw = int(h / factor), int(w / factor)
    frame_zoom = frame[(h - nh) // 2:(h + nh) // 2, (w - nw) // 2:(w + nw) // 2]
    return cv2.resize(frame_zoom, (w, h))

def eliminar_ruido(frame):
    return cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)

def aplicar_filtros_basicos(frame, filtro):
    if filtro == "blanco_negro":
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif filtro == "rgb":
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    elif filtro == "escala_grises":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.merge([gray, gray, gray])
    else:
        return frame

def generar_versiones(output_folder, base_name, frame):
    transformaciones = {
        "rotacion_volteo": lambda img: cv2.flip(cv2.rotate(img, cv2.ROTATE_180), 1),
        "brillo_contraste": lambda img: ajustar_brillo_contraste(img, alpha=1.5, beta=30),
        "desplazamiento_zoom": lambda img: aplicar_zoom(img, factor=1.3),
        "recorte": lambda img: recortar_aleatoriamente(img, porcentaje=0.2),
        "eliminacion_ruido": lambda img: eliminar_ruido(img),
        "filtro_bn": lambda img: aplicar_filtros_basicos(img, "blanco_negro"),
        "filtro_rgb": lambda img: aplicar_filtros_basicos(img, "rgb"),
        "filtro_grises": lambda img: aplicar_filtros_basicos(img, "escala_grises"),
        "espejo": lambda img: cv2.flip(img, 1),
        "brillo_alto": lambda img: ajustar_brillo_contraste(img, alpha=2.0, beta=50),
        "brillo_medio": lambda img: ajustar_brillo_contraste(img, alpha=1.5, beta=25),
        "brillo_bajo": lambda img: ajustar_brillo_contraste(img, alpha=0.8, beta=-30),
        "contraste_alto": lambda img: ajustar_brillo_contraste(img, alpha=2.5, beta=0),
        "contraste_bajo": lambda img: ajustar_brillo_contraste(img, alpha=0.5, beta=0)
    }

    for nombre, transformacion in transformaciones.items():
        img_transformada = transformacion(frame)
        cv2.imwrite(f"{output_folder}/{base_name}_{nombre}.jpg", img_transformada)

def generar_dataset(video_path, output_folder, resolution=(28, 21)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error al abrir el video.")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    print(f"Duración del video: {duration:.2f} segundos")

    frame_count = 0
    img_count = 0

    cv2.namedWindow("Procesamiento", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Procesamiento", 600, 400)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Procesamiento", frame)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            print("Ejecución detenida")
            break

        img_resized = cv2.resize(frame, resolution)

        base_name = f"frame_{img_count}"
        cv2.imwrite(f"{output_folder}/{base_name}.jpg", img_resized)

        generar_versiones(output_folder, base_name, img_resized)

        img_count += 1
        frame_count += 1
        print(f"Procesando frame {frame_count}/{total_frames}...")

    cap.release()
    cv2.destroyAllWindows()
    print(f"Dataset generado en {output_folder}")


video_path = "C:/Users/ShiEu/Downloads/FP1 ‐ Hecho con Clipchamp (1).MP4" 
output_folder = "C:/Users/ShiEu/Documents/dataset_coches"

generar_dataset(video_path, output_folder)
