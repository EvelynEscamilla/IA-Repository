import pygame
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Input # type: ignore

# Definición del modelo
model = Sequential([
    Input(shape=(2,)),  
    Dense(10, activation='relu'),
    Dense(1, activation='sigmoid')  
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None

# Variables de salto
salto = False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('Proyecto2/assets/sprites/mono_frame_1.png'),
    pygame.image.load('Proyecto2/assets/sprites/mono_frame_2.png'),
    pygame.image.load('Proyecto2/assets/sprites/mono_frame_3.png'),
    pygame.image.load('Proyecto2/assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('Proyecto2/assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('Proyecto2/assets/game/fondo2.png')
nave_img = pygame.image.load('Proyecto2/assets/game/ufo.png')
menu_img = pygame.image.load('Proyecto2/assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -10  # Velocidad de la bala hacia la izquierda
bala_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -3) 
        bala_disparada = True

def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  
    bala_disparada = False

def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  
        salto_altura -= gravedad 

        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  
            en_suelo = True

def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2

    fondo_x1 -= 1
    fondo_x2 -= 1

    if fondo_x1 <= -w:
        fondo_x1 = w

    if fondo_x2 <= -w:
        fondo_x2 = w

    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    pantalla.blit(nave_img, (nave.x, nave.y))

    if bala_disparada:
        bala.x += velocidad_bala

    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()  

def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x) 
    velocidad_bala_abs = abs(velocidad_bala)
    salto_hecho = 1 if salto else 0  
    datos_modelo.append((velocidad_bala_abs, distancia, salto_hecho))

def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

def mostrar_submenu_auto():
    global menu_activo, modo_auto
    pantalla.fill(NEGRO)
    texto = fuente.render("Selecciona una opción: 'D' para Árbol de decisión, 'R' para Red neuronal", True, BLANCO)
    pantalla.blit(texto, (w // 8, h // 2))
    pygame.display.flip()

    submenu_activo = True  

    while submenu_activo:  
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_d:
                    print("Árbol de decisión seleccionado")
                    modo_auto = True
                    submenu_activo = False 
                    arbol_decision()  
                elif evento.key == pygame.K_r:
                    print("Red neuronal seleccionada")
                    modo_auto = True
                    submenu_activo = False  
                    red_neuronal()

                elif evento.key == pygame.K_q:
                    print("Juego terminado.")
                    submenu_activo = False
                    mostrar_menu()


def mostrar_menu():
    global menu_activo, modo_auto, datos_modelo
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona 'A' para Auto, 'M' para Manual, o 'Q' para Salir", True, BLANCO)
    pantalla.blit(texto, (w // 4, h // 2))
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    modo_auto = True
                    menu_activo = False
                    mostrar_submenu_auto()  
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    datos_modelo = []
                    menu_activo = False
                elif evento.key == pygame.K_q:
                    print("Juego terminado.")
                    pygame.quit()
                    exit()

def entrenar_arbol_decision():
    dataset = pd.DataFrame(datos_modelo, columns=['velocidad_bala', 'distancia', 'salto_hecho'])
    
    X = dataset.iloc[:, :2] 
    y = dataset.iloc[:, 2]   
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = DecisionTreeClassifier()
    
    clf.fit(X_train, y_train)
    
    return clf

def predecir_accion(model, velocidad_bala, distancia):
    datos_entrada = np.array([[velocidad_bala, distancia]])
    prediccion = model.predict(datos_entrada)
    return prediccion


def arbol_decision():
    global modo_auto, jugador, bala, salto, en_suelo, menu_activo

    # Entrenar el árbol de decisión
    clf = entrenar_arbol_decision()

    while modo_auto:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    print("Regresando al menú principal.")
                    modo_auto = False
                    menu_activo = True
                    mostrar_menu()
                    return

        distancia = abs(jugador.x - bala.x)
        velocidad_bala_abs = abs(velocidad_bala)

        accion = predecir_accion(clf, velocidad_bala_abs, distancia)

        if accion == 1:
            if en_suelo:
                salto = True
                en_suelo = False

        if salto:
            manejar_salto()

        if jugador.y >= h - 100:
            jugador.y = h - 100
            if not en_suelo:
                en_suelo = True
                salto = False

        if not bala_disparada:
            disparar_bala()

        update()

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def crear_red_neuronal():
    print("Lista: " ,datos_modelo)
    model = Sequential([
        Dense(8, input_dim=2, activation='relu'),
        Dense(4, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    return model

def entrenar_red_neuronal():
    dataset = pd.DataFrame(datos_modelo, columns=['velocidad_bala', 'distancia', 'salto_hecho'])
    
    X = dataset.iloc[:, :2].values
    y = dataset.iloc[:, 2].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = crear_red_neuronal()
    model.fit(X_train, y_train, epochs=40, batch_size=64, verbose=1)
    
    return model

def predecir_accionN(model, velocidad_bala, distancia):
    prediccion = model.predict(np.array([[velocidad_bala, distancia]]))
    return int(prediccion[0][0] > 0.3)

def red_neuronal():
    global modo_auto, jugador, bala, salto, en_suelo, menu_activo
    
    model = entrenar_red_neuronal()

    while modo_auto:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    print("Regresando al menú principal.")
                    modo_auto = False
                    menu_activo = True
                    mostrar_menu()
                    return

        distancia = abs(jugador.x - bala.x)
        velocidad_bala_abs = abs(velocidad_bala)

        accion = predecir_accionN(model, velocidad_bala_abs, distancia)

        if accion == 1:
            if en_suelo:
                salto = True
                en_suelo = False

        if salto:
            manejar_salto()

        if jugador.y >= 400 - 100:
            jugador.y = 400 - 100
            if not en_suelo:
                en_suelo = True
                salto = False

        if not bala_disparada:
            disparar_bala()

        update()
        pygame.display.flip()
        pygame.time.Clock().tick(30)

def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    menu_activo = True
    jugador.x, jugador.y = 50, h - 100
    bala.x = w - 50
    nave.x, nave.y = w - 100, h - 100
    bala_disparada = False
    salto = False
    en_suelo = True
    print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()

def main():
    global salto, en_suelo, bala_disparada, menu_activo

    reloj = pygame.time.Clock()
    mostrar_menu()
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:
                    pausa_juego()
                if evento.key == pygame.K_q:
                    print("Regresando al menú principal.")
                    menu_activo = True
                    mostrar_menu()

        if not pausa and not menu_activo:
            if not modo_auto:
                if salto:
                    manejar_salto()
                guardar_datos()

            if not bala_disparada:
                disparar_bala()
            update()

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
