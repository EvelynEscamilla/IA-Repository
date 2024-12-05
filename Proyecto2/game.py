import pygame
import random
import csv

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, balas, nave, fondo, etc.
jugador = None
bala_horizontal = None
bala_vertical = None
fondo = None
nave = None
menu = None

# Variables de salto
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False

# Lista para guardar los datos de velocidad, distancia y salto
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

# Crear el rectángulo del jugador y de las balas
jugador = pygame.Rect(50, h - 100, 32, 48)
bala_horizontal = pygame.Rect(w - 50, h - 90, 16, 16)
bala_vertical = pygame.Rect(jugador.x + 8, 0, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10
frame_count = 0

# Variables para las balas
velocidad_bala_horizontal = -10
velocidad_bala_vertical = 5
bala_horizontal_disparada = False
bala_vertical_disparada = False

# Variables de la nueva bala diagonal
bala_diagonal = None
bala_diagonal_disparada = False
velocidad_bala_diagonal = 5
gravedad_bala_diagonal = 1  # Velocidad de caída

# Crear el rectángulo de la nueva bala diagonal
bala_diagonal = pygame.Rect(w, random.randint(0, h - 20), 16, 16)

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Función para disparar la bala horizontal
def disparar_bala_horizontal():
    global bala_horizontal_disparada, velocidad_bala_horizontal
    if not bala_horizontal_disparada:
        velocidad_bala_horizontal = random.randint(-8, -3)
        bala_horizontal_disparada = True

# Función para disparar la bala vertical
def disparar_bala_vertical():
    global bala_vertical_disparada, velocidad_bala_vertical
    if not bala_vertical_disparada:
        velocidad_bala_vertical = random.randint(3, 8)
        bala_vertical_disparada = True
        
# Función para disparar la bala diagonal
def disparar_bala_diagonal():
    global bala_diagonal_disparada
    if not bala_diagonal_disparada:
        bala_diagonal.y = random.randint(0, h - 20)  # Altura aleatoria al disparar
        bala_diagonal.x = w  # Comenzar desde la derecha
        bala_diagonal_disparada = True

# Función para reiniciar la posición de la bala horizontal
def reset_bala_horizontal():
    global bala_horizontal, bala_horizontal_disparada
    bala_horizontal.x = w - 50
    bala_horizontal_disparada = False

# Función para reiniciar la posición de la bala vertical
def reset_bala_vertical():
    global bala_vertical, bala_vertical_disparada
    bala_vertical.y = 0
    bala_vertical.x = jugador.x + 8  # Colocar la bala vertical en la posición del jugador
    bala_vertical_disparada = False

# Función para reiniciar la posición de la bala diagonal
def reset_bala_diagonal():
    global bala_diagonal, bala_diagonal_disparada
    bala_diagonal.x = w
    bala_diagonal.y = random.randint(0, h - 20)  # Reiniciar en altura aleatoria
    bala_diagonal_disparada = False

# Función para manejar el salto
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

# Función para actualizar el juego
def update():
    global bala_horizontal, bala_vertical, bala_diagonal
    global velocidad_bala_horizontal, velocidad_bala_vertical
    global current_frame, frame_count, fondo_x1, fondo_x2
    
    # Mover y dibujar la bala diagonal
    if bala_diagonal_disparada:
        bala_diagonal.x -= velocidad_bala_diagonal  # Mover hacia la izquierda
        bala_diagonal.y += gravedad_bala_diagonal    # Caer hacia abajo
        
    if bala_diagonal.x < 0 or bala_diagonal.y > h:  # Reiniciar si sale de la pantalla
        reset_bala_diagonal()
    
    pantalla.blit(bala_img, (bala_diagonal.x, bala_diagonal.y))

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    if fondo_x1 <= -w:
        fondo_x1 = w
    if fondo_x2 <= -w:
        fondo_x2 = w

    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala horizontal
    if bala_horizontal_disparada:
        bala_horizontal.x += velocidad_bala_horizontal
    if bala_horizontal.x < 0:
        reset_bala_horizontal()
    pantalla.blit(bala_img, (bala_horizontal.x, bala_horizontal.y))

    # Mover y dibujar la bala vertical
    if bala_vertical_disparada:
        bala_vertical.y += velocidad_bala_vertical
    if bala_vertical.y > h:
        reset_bala_vertical()
    pantalla.blit(bala_img, (bala_vertical.x, bala_vertical.y))
    
    # Mover y dibujar la bala diagonal
    if bala_diagonal_disparada:
        bala_diagonal.x -= velocidad_bala_diagonal
    if bala_diagonal.x < 0:
        reset_bala_diagonal()
    pantalla.blit(bala_img, (bala_diagonal.x, bala_diagonal.y))

    # Colisión entre el jugador y las balas
    if jugador.colliderect(bala_horizontal) or jugador.colliderect(bala_vertical) or jugador.colliderect(bala_diagonal):
        print("Colisión detectada!")
        reiniciar_juego()

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala_horizontal, velocidad_bala_horizontal, salto
    distancia = abs(jugador.x - bala_horizontal.x)
    salto_hecho = 1 if salto else 0
    datos_modelo.append((velocidad_bala_horizontal, distancia, salto_hecho))

def guardar_datos_csv():
    with open('datos_juego.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['velocidad_bala', 'distancia', 'salto_hecho'])
        writer.writerows(datos_modelo)
    print("Datos guardados en datos_juego.csv")

# Función para pausar el juego
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

# Función para mostrar el menú
def mostrar_menu():
    global menu_activo, modo_auto
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
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

# Función para reiniciar el juego
def reiniciar_juego():
    global menu_activo, jugador, bala_horizontal, bala_vertical, nave, bala_horizontal_disparada, salto, en_suelo
    menu_activo = True
    jugador.x, jugador.y = 50, h - 100
    bala_horizontal.x = w - 50
    bala_vertical.y = 0
    bala_vertical.x = jugador.x + 8  # Colocar la bala vertical en la posición del jugador
    nave.x, nave.y = w - 100, h - 100
    bala_horizontal_disparada = False
    salto = False
    en_suelo = True
    print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()
    guardar_datos_csv()

# Actualiza el main
def main():
    global salto, en_suelo, bala_horizontal_disparada, bala_vertical_disparada, bala_diagonal_disparada
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
                if evento.key == pygame.K_RETURN:
                    disparar_bala_horizontal()
                    disparar_bala_vertical()
                    disparar_bala_diagonal()  # Dispara la bala diagonal
        if not pausa:
            teclas = pygame.key.get_pressed() 
            if not modo_auto:
                if not bala_horizontal_disparada:
                    disparar_bala_horizontal()
                if not bala_vertical_disparada:
                    disparar_bala_vertical()
                if not bala_diagonal_disparada:
                    disparar_bala_diagonal()
                if teclas[pygame.K_LEFT] and jugador.x > 0:
                    jugador.x -= 5
                if teclas[pygame.K_RIGHT] and jugador.x < w - jugador.width:
                    jugador.x += 5
                guardar_datos()
            

            manejar_salto()
            update()
            pygame.display.flip()
            reloj.tick(30)

    guardar_datos_csv()
    pygame.quit()

if __name__ == "__main__":
    main()
