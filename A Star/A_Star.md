### Algoritmo A*
Para iniciar con el Algoritmo A asterisco el profesor nos proporciono el siguiente pseudocodigo:
```
Function A*(inicio, objetivo)
    crear una cola de prioridad `open_set`
    agregar `inicio` a `open_set` con f(inicio) = h(inicio)
    
    g_score[inicio] = 0
    f_score[inicio] = h(inicio)  // Heurística desde inicio hasta objetivo

    While `open_set` no esté vacío:
        current = nodo en `open_set` con menor valor de f_score
        If current == objetivo:
            return reconstruir_camino(current)  // Camino encontrado

        quitar current de `open_set`

        For cada vecino de current:
            tentative_g_score = g_score[current] + costo para moverse a vecino
            
            If tentative_g_score < g_score[vecino]:  // Mejor camino encontrado
                came_from[vecino] = current
                g_score[vecino] = tentative_g_score
                f_score[vecino] = g_score[vecino] + h(vecino, objetivo)
                
                If vecino no está en `open_set`:
                    agregar vecino a `open_set`

    Return fracaso  // Si no se encuentra un camino
```
El algoritmo A* es un algoritmo de búsqueda de los mas populares; se utiliza para encontrar el camino mas corto entre dos puntos. 
Para encontrar el camino mas corto el algoritmo utiliza funciones de evaluación a través de dos valores clave:
***g(h):*** el costo real desde el nodo inicial hasta el nodo actual n.
***h(n):*** la estimación heuristica del costo del nodo actual n hasta el nodo final.
***f(n):*** función de evaluación que se define como ***g(n) + h(n)*** en esta función g(n) es el costo acumulado y h(n) la estimación heuristica.

El profesor también nos proporciono el siguiente código cascarón para comenzar la creación del algoritmo A*:
´´´
import pygame
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

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

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def main(ventana, ancho):
    FILAS = 10
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

    pygame.quit()
main(VENTANA, ANCHO_VENTANA)
´´´