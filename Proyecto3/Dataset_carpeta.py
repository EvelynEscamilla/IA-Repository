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

def rotar_y_redimensionar(frame, angulo_max=30, tamaño=(128, 128)):
    angulo = np.random.uniform(-angulo_max, angulo_max)
    
    h, w = frame.shape[:2]
    centro = (w // 2, h // 2)
    
    matriz_rotacion = cv2.getRotationMatrix2D(centro, angulo, 1)
    
    imagen_rotada = cv2.warpAffine(frame, matriz_rotacion, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    
    imagen_redimensionada = cv2.resize(imagen_rotada, tamaño)
    
    return imagen_redimensionada

def rotar_varias_veces(frame, angulos=[15, 30, 45, 60, 90], tamaño=(128, 128)):
    rotaciones = []
    for angulo in angulos:
        rotacion = rotar_y_redimensionar(frame, angulo_max=angulo, tamaño=tamaño)
        rotaciones.append(rotacion)
    return rotaciones

def cambiar_tono_saturacion(frame, alpha=1.2, beta=50):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv[..., 0] = hsv[..., 0] * alpha + beta 
    hsv[..., 1] = hsv[..., 1] * alpha         
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def agregar_ruido_sal_pimienta(frame, cantidad=0.02):
    h, w = frame.shape[:2]
    salida = np.copy(frame)
    num_pixeles = int(cantidad * h * w)
    
    for _ in range(num_pixeles):
        x, y = np.random.randint(0, w), np.random.randint(0, h)
        salida[y, x] = np.random.choice([0, 255], size=3)
    
    return salida

def desenfoque_gaussiano(frame, kernel_size=(5, 5)):
    return cv2.GaussianBlur(frame, kernel_size, 0)

def escala_color(frame, factor=1.0):
    return cv2.convertScaleAbs(frame, alpha=factor, beta=0)

def version_espejo(frame):
    return cv2.flip(frame, 1)

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
        "brillo_alto": lambda img: ajustar_brillo_contraste(img, alpha=2.0, beta=50),
        "brillo_medio": lambda img: ajustar_brillo_contraste(img, alpha=1.5, beta=25),
        "brillo_bajo": lambda img: ajustar_brillo_contraste(img, alpha=0.8, beta=-30),
        "contraste_alto": lambda img: ajustar_brillo_contraste(img, alpha=2.5, beta=0),
        "contraste_bajo": lambda img: ajustar_brillo_contraste(img, alpha=0.5, beta=0),
        "rotacion_aleatoria": lambda img: rotar_y_redimensionar(img),
        "rotaciones_adicionales": lambda img: rotar_varias_veces(img),
        "cambiar_tono_saturacion": lambda img: cambiar_tono_saturacion(img),
        "ruido_sal_pimienta": lambda img: agregar_ruido_sal_pimienta(img),
        "desenfoque_gaussiano": lambda img: desenfoque_gaussiano(img),
        "escala_color": lambda img: escala_color(img),
        "espejo": lambda img: version_espejo(img) 
    }

    for nombre, transformacion in transformaciones.items():
        img_transformada = transformacion(frame)
        if isinstance(img_transformada, list): 
            for i, img in enumerate(img_transformada):
                cv2.imwrite(f"{output_folder}/{base_name}_{nombre}_{i}.jpg", img)
        else:
            cv2.imwrite(f"{output_folder}/{base_name}_{nombre}.jpg", img_transformada)

    frame_espejo = version_espejo(frame)

    for nombre, transformacion in transformaciones.items():
        img_transformada = transformacion(frame_espejo)
        if isinstance(img_transformada, list):  
            for i, img in enumerate(img_transformada):
                cv2.imwrite(f"{output_folder}/{base_name}_{nombre}_espejo_{i}.jpg", img)
        else:
            cv2.imwrite(f"{output_folder}/{base_name}_{nombre}_espejo.jpg", img_transformada)

def generar_dataset_imagenes(input_folder, output_folder, resolution=(128, 128)):
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

input_folder = "C:/Users/ShiEu/Documents/9 Semestre/imagenes"
output_folder = "C:/Users/ShiEu/Documents/dataset_coches"

generar_dataset_imagenes(input_folder, output_folder)
