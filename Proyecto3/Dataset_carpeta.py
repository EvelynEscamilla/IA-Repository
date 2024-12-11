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
    }

    for nombre, transformacion in transformaciones.items():
        img_transformada = transformacion(frame)
        cv2.imwrite(f"{output_folder}/{base_name}_{nombre}.jpg", img_transformada)

def generar_dataset_imagenes(input_folder, output_folder, resolution=(28, 21)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for img_name in os.listdir(input_folder):
        img_path = os.path.join(input_folder, img_name)
        if not os.path.isfile(img_path):
            continue

        frame = cv2.imread(img_path)
        if frame is None:
            print(f"No se pudo leer la imagen: {img_name}")
            continue

        frame_resized = cv2.resize(frame, resolution)

        base_name, _ = os.path.splitext(img_name)
        cv2.imwrite(f"{output_folder}/{base_name}_original.jpg", frame_resized)

        generar_versiones(output_folder, base_name, frame_resized)
        print(f"Procesada la imagen: {img_name}")

    print(f"Dataset generado en {output_folder}")

# Configuración de carpetas
input_folder = "C:/Users/ShiEu/Documents/9 Semestre/imagenes"
output_folder = "C:/Users/ShiEu/Documents/dataset_coches"

generar_dataset_imagenes(input_folder, output_folder)
