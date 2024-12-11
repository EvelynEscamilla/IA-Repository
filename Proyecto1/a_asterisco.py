import pygame
import tkinter as tk
from tkinter import ttk, messagebox
import random
import heapq

pygame.font.init()
FUENTE = pygame.font.SysFont("arial", 15)

# Configuraciones iniciales de Pygame
ANCHO_VENTANA = 600
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (102, 255, 102)
AZUL = (135, 206, 250)
MORADO_SUAVE = (200, 150, 255) 

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.g = float('inf')  
        self.h = 0 
        self.f = float('inf')  
        self.padre = None  

    def __lt__(self, other):
        return self.f < other.f 
    
    def dibujar_texto(self, ventana):
        if self.color != BLANCO and self.color != NEGRO:
            g_valor = int(self.g) if self.g < float('inf') else "-"
            h_valor = int(self.h) if self.h < float('inf') else "-"
            f_valor = int(self.f) if self.f < float('inf') else "-"

            g_texto = FUENTE.render(f"g:{g_valor}", True, NEGRO)
            h_texto = FUENTE.render(f"h:{h_valor}", True, NEGRO)
            f_texto = FUENTE.render(f"f:{f_valor}", True, NEGRO)

            ventana.blit(g_texto, (self.x + 2, self.y + 2)) 
            ventana.blit(h_texto, (self.x + 2, self.y + self.ancho // 2)) 
            ventana.blit(f_texto, (self.x + self.ancho // 2, self.y + self.ancho // 2))

    #posicion del nodo
    def get_pos(self):
        return self.fila, self.col

    #condicionales para el tipo de nodo
    def es_pared(self):
        return self.color == NEGRO 

    def es_inicio(self):
        return self.color == VERDE

    def es_fin(self):
        return self.color == AZUL

    #tablero
    def restablecer(self):
        self.color = BLANCO
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.padre = None

    #Se define el tipo de nodo
    def hacer_inicio(self):
        self.color = VERDE

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = AZUL

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))


#Creacion del tablero
def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)
            nodo.dibujar_texto(ventana)  
    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

#posicion del cuadro que se selecciona
def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

#Paredes aleatorias
def generar_paredes_aleatorias(grid, filas):
    for i in range(filas):
        for j in range(filas):
            if random.random() < 0.3:  
                grid[i][j].hacer_pared()

#Pestaña para pedir los datos
# Pestaña para pedir los datos
def pedir_valores_iniciales():
    root = tk.Tk()
    root.title("Configuración Inicial")

    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, expand=True)

    config_frame = ttk.Frame(notebook, width=400, height=200)
    config_frame.pack(fill='both', expand=True)

    notebook.add(config_frame, text="Configuración")

    ttk.Label(config_frame, text="Tamaño del tablero (3-10):").grid(row=0, column=0, pady=10, padx=10, sticky="w")
    
    # Variables de control con valores iniciales
    tamano_var = tk.StringVar(value="10")
    tipo_var = tk.StringVar(value="1")
    
    # Entradas con valores iniciales
    entry_tamano = ttk.Entry(config_frame, textvariable=tamano_var)
    entry_tamano.grid(row=0, column=1, pady=10, padx=10)

    ttk.Label(config_frame, text="Tipo de generación (1: Manual, 2: Aleatoria):").grid(row=1, column=0, pady=10, padx=10, sticky="w")
    entry_tipo = ttk.Entry(config_frame, textvariable=tipo_var)
    entry_tipo.grid(row=1, column=1, pady=10, padx=10)

    valores = {"tamano": 10, "tipo": "1"}

    # Función para validar y confirmar los valores
    def confirmar():
        tamano = tamano_var.get()
        tipo_generacion = tipo_var.get()

        if not tamano.isdigit() or not (3 <= int(tamano) <= 10):
            messagebox.showerror("Error", "El tamaño del tablero debe ser un número entre 3 y 10.")
            return

        if tipo_generacion not in {"1", "2"}:
            messagebox.showerror("Error", "El tipo de generación debe ser 1 (Manual) o 2 (Aleatoria).")
            return

        valores["tamano"] = int(tamano)
        valores["tipo"] = tipo_generacion
        root.destroy()

    ttk.Button(config_frame, text="Confirmar", command=confirmar).grid(row=2, column=0, columnspan=2, pady=20)

    root.mainloop()

    return valores["tamano"], valores["tipo"]

#A*
#Distancia inicio-fin
def calcular_heuristica(nodo, fin):
    dx = abs(nodo.fila - fin.fila)
    dy = abs(nodo.col - fin.col)
    return max(dx, dy) + (1.41 - 1) * min(dx, dy)


def vecinos(nodo, grid):
    vecinos = []
    filas, cols = len(grid), len(grid[0])
    
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1),  
                (-1, -1), (-1, 1), (1, -1), (1, 1)]  
    
    for dx, dy in direcciones:
        x, y = nodo.fila + dx, nodo.col + dy
        if 0 <= x < filas and 0 <= y < cols:
            if abs(dx) + abs(dy) == 2:  #diagonal
                if grid[nodo.fila][nodo.col + dy].es_pared() and grid[nodo.fila + dx][nodo.col].es_pared():
                    continue
            vecinos.append(grid[x][y])
    
    return vecinos


def reconstruir_camino(came_from, nodo, ventana, grid, inicio, fin):
    camino = []
    
    while nodo in came_from:
        camino.append(nodo)
        nodo = came_from[nodo]
    
    camino.append(inicio)
    
    for nodo in reversed(camino):  
        if nodo != inicio and nodo != fin:
            nodo.color = MORADO_SUAVE
        dibujar(ventana, grid, len(grid), ANCHO_VENTANA)
        pygame.time.delay(100)  

def algoritmo_a_asterisco(ventana, grid, inicio, fin):
    open_set = []
    heapq.heappush(open_set, (inicio.f, inicio))
    came_from = {}

    inicio.g = 0
    inicio.f = calcular_heuristica(inicio, fin)
    


    while open_set:
        _, nodo_actual = heapq.heappop(open_set)

        if nodo_actual == fin:
            reconstruir_camino(came_from, nodo_actual, ventana, grid, inicio, fin)
            return True

        if nodo_actual != inicio and nodo_actual != fin:
            nodo_actual.color = (255, 255, 0)

        for vecino in vecinos(nodo_actual, grid):
            if vecino.es_pared():
                continue
            
            dx = vecino.x - nodo_actual.x
            dy = vecino.y - nodo_actual.y

            tentativo_g = nodo_actual.g + (1.41 if abs(dx) + abs(dy) == 2 else 1)


            if tentativo_g < vecino.g:
                came_from[vecino] = nodo_actual
                vecino.g = tentativo_g
                vecino.h = calcular_heuristica(vecino, fin)
                vecino.f = vecino.g + vecino.h
                heapq.heappush(open_set, (vecino.f, vecino))

        dibujar(ventana, grid, len(grid), ANCHO_VENTANA)
        pygame.time.delay(150)

    return False

def main():
    tamano_tablero, tipo_generacion = pedir_valores_iniciales()

    grid = crear_grid(tamano_tablero, ANCHO_VENTANA)

    if tipo_generacion == "2":
        generar_paredes_aleatorias(grid, tamano_tablero)
        puede_dibujar_paredes = False  
    else:
        puede_dibujar_paredes = True  

    inicio = None
    fin = None
    dibujando_pared = False

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                fila, col = obtener_click_pos(pygame.mouse.get_pos(), tamano_tablero, ANCHO_VENTANA)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    nodo.hacer_inicio()
                elif not fin and nodo != inicio:
                    fin = nodo
                    nodo.hacer_fin()
                elif nodo != fin and nodo != inicio and puede_dibujar_paredes: 
                    nodo.hacer_pared()
                dibujando_pared = True

            elif evento.type == pygame.MOUSEBUTTONUP:
                dibujando_pared = False

            if evento.type == pygame.MOUSEMOTION and dibujando_pared and puede_dibujar_paredes:
                fila, col = obtener_click_pos(pygame.mouse.get_pos(), tamano_tablero, ANCHO_VENTANA)
                nodo = grid[fila][col]
                if nodo != inicio and nodo != fin:
                    nodo.hacer_pared()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and inicio and fin:
                    algoritmo_a_asterisco(VENTANA, grid, inicio, fin)
                    puede_dibujar_paredes = False  

                if evento.key == pygame.K_r:
                    for fila in grid:
                        for nodo in fila:
                            nodo.restablecer()

                    inicio = None
                    fin = None

                    if tipo_generacion == "2":
                        generar_paredes_aleatorias(grid, tamano_tablero)  
                        puede_dibujar_paredes = False  
                    else:
                        puede_dibujar_paredes = True  

        dibujar(VENTANA, grid, tamano_tablero, ANCHO_VENTANA)

    pygame.quit()


if __name__ == "__main__":
    main()
