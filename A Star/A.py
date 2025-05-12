# visualizador_a_estrella.py

import pygame
import heapq
import tkinter as tk
from tkinter import Frame, Text, Scrollbar, VERTICAL, RIGHT, LEFT, Y, BOTH
import string

# ----- Colores -----
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AZUL = (0, 0, 255)

# ----- Generar IDs como en Excel -----
def generar_ids_excel(filas, columnas):
    letras = list(string.ascii_lowercase)
    ids = []
    for i in range(filas * columnas):
        if i < 26:
            ids.append(letras[i])
        else:
            ids.append(letras[(i // 26) - 1] + letras[i % 26])
    return ids


class Nodo:
    def __init__(self, fila, col, ancho, total_filas, id_excel):
        self.fila = fila
        self.col = col
        self.id_excel = id_excel
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.g = float("inf")
        self.h = 0
        self.padre = None

    def __lt__(self, otro):
        return (self.g + self.h) < (otro.g + otro.h)

    def get_pos(self):
        return self.fila, self.col

    # Verificar tipo de nodo
    def es_pared(self): return self.color == NEGRO
    def es_inicio(self): return self.color == NARANJA
    def es_fin(self): return self.color == PURPURA

    # Establecer el tipo de nodo
    def restablecer(self): self.color = BLANCO
    def hacer_inicio(self): self.color = NARANJA
    def hacer_pared(self): self.color = NEGRO
    def hacer_fin(self): self.color = PURPURA

    def hacer_camino(self):
        if not self.es_fin() and not self.es_inicio():
            self.color = VERDE

    def dibujar(self, ventana, fuente):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
        texto = fuente.render(self.id_excel, True, NEGRO)
        ventana.blit(texto, (self.x + 5, self.y + 5))

# ----- Ventana Informativa -----
class VentanaInformacion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Valores del Camino Óptimo")
        self.root.geometry("400x700")

        self.label_abierta = tk.Label(self.root, text="Lista Abierta", font=("Arial", 12, "bold"))
        self.label_abierta.pack()
        self.lista_abierta = tk.Listbox(self.root, font=("Consolas", 10), height=10)
        self.lista_abierta.pack(fill=tk.BOTH, expand=True)

        self.label_cerrada = tk.Label(self.root, text="Lista Cerrada", font=("Arial", 12, "bold"))
        self.label_cerrada.pack()
        self.lista_cerrada = tk.Listbox(self.root, font=("Consolas", 10), height=10)
        self.lista_cerrada.pack(fill=tk.BOTH, expand=True)

        self.label_camino = tk.Label(self.root, text="Camino Óptimo", font=("Arial", 12, "bold"))
        self.label_camino.pack()
        self.lista_camino = tk.Listbox(self.root, font=("Consolas", 10), fg="green", height=10)
        self.lista_camino.pack(fill=tk.BOTH, expand=True)

    def actualizar(self, abiertos, cerrados, camino):
        # Lista abierta
        self.lista_abierta.delete(0, tk.END)
        for nodo in abiertos:
            texto = f"ID: {nodo.id_excel} | G: {int(nodo.g)} | H: {int(nodo.h)} | F: {int(nodo.g + nodo.h)}"
            self.lista_abierta.insert(tk.END, texto)

        # Lista cerrada
        self.lista_cerrada.delete(0, tk.END)
        for nodo in cerrados:
            texto = f"ID: {nodo.id_excel} | G: {int(nodo.g)} | H: {int(nodo.h)} | F: {int(nodo.g + nodo.h)}"
            self.lista_cerrada.insert(tk.END, texto)

        # Camino óptimo
        self.lista_camino.delete(0, tk.END)
        for nodo in camino:
            texto = f"ID: {nodo.id_excel} | G: {int(nodo.g)} | H: {int(nodo.h)} | F: {int(nodo.g + nodo.h)}"
            self.lista_camino.insert(tk.END, texto)

        self.root.update()

# ----- Configuración de la ventana Pygame -----
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de A*")

# ----- Funciones de visualización -----
def crear_grid(filas, ancho):
    grid = []
    ids = generar_ids_excel(filas, filas)
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas, ids[i * filas + j])
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho, fuente):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana, fuente)
    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def heuristica(nodo1, nodo2):
    x1, y1 = nodo1.get_pos()
    x2, y2 = nodo2.get_pos()
    return (abs(x1 - x2) + abs(y1 - y2)) * 10

def reconstruir_camino(nodo_final):
    actual = nodo_final.padre
    camino = []
    while actual and actual.padre:
        actual.hacer_camino()
        camino.append(actual)
        actual = actual.padre
    camino.reverse()
    return camino

def a_estrella(grid, inicio, fin, ventana, filas, ancho, fuente, ventana_info):
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    open_set = []
    heapq.heappush(open_set, (0, inicio))
    inicio.g = 0
    inicio.h = heuristica(inicio, fin)
    lista_cerrada = set()
    abiertos = []
    cerrados = []

    while open_set:
        _, nodo_actual = heapq.heappop(open_set)
        if nodo_actual in lista_cerrada:
            continue

        lista_cerrada.add(nodo_actual)
        cerrados.append(nodo_actual)

        if nodo_actual == fin:
            camino = reconstruir_camino(fin)
            ventana_info.actualizar(abiertos, cerrados, camino)
            return

        for dx, dy in direcciones:
            fila, col = nodo_actual.fila + dx, nodo_actual.col + dy
            if 0 <= fila < filas and 0 <= col < filas:
                vecino = grid[fila][col]
                if vecino.es_pared() or vecino in lista_cerrada:
                    continue

                nuevo_g = nodo_actual.g + (14 if dx != 0 and dy != 0 else 10)

                if nuevo_g < vecino.g:
                    vecino.g = nuevo_g
                    vecino.h = heuristica(vecino, fin)
                    vecino.padre = nodo_actual
                    heapq.heappush(open_set, (vecino.g + vecino.h, vecino))
                    if vecino != inicio and vecino != fin:
                        vecino.color = AZUL
                        abiertos.append(vecino)

        dibujar(ventana, grid, filas, ancho, fuente)

        for nodo in lista_cerrada:
            if nodo != inicio and nodo != fin:
                nodo.color = ROJO

        ventana_info.actualizar(abiertos, cerrados, [])

# ----- Programa Principal -----
def main(ventana, ancho):
    pygame.font.init()
    fuente = pygame.font.Font(None, 18)
    FILAS = 9
    grid = crear_grid(FILAS, ancho)
    inicio = None
    fin = None
    corriendo = True

    ventana_info = VentanaInformacion()

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho, fuente)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Botón izquierdo del mouse
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio:
                    inicio = nodo
                    inicio.hacer_inicio()
                elif not fin:
                    fin = nodo
                    fin.hacer_fin()
                else:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Botón derecho del mouse
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    a_estrella(grid, inicio, fin, ventana, FILAS, ancho, fuente, ventana_info)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)
