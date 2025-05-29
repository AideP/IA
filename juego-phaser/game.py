import pygame
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

pygame.init()

# --- CONFIGURACIÓN DE PANTALLA ---
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))

# --- COLORES ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 30, 30)

# --- ESTADOS DEL JUEGO ---
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True
menu_activo = True
modo_auto = False
modo_modelo = None  # 'arbol', 'nn', 'knn'

# --- DATOS Y MODELOS PARA ML ---
datos_salto = []            # (vel_bala, dx, salto)
datos_movimiento = []       # ((dx, x_jugador, x_bala_vertical), accion)

# Modelos
modelo_salto_arbol = None
modelo_movimiento_arbol = None
modelo_salto_nn = None
modelo_movimiento_nn = None
modelo_salto_knn = None
modelo_movimiento_knn = None

# --- CONTROL DE MOVIMIENTO ---
accion_actual = 0
tiempo_accion = 0
UMBRAL_TIEMPO = 10
UMBRAL_PELIGRO = 50

# --- POSICIONES Y OBJETOS ---
POSICION_ORIGEN = 50
jugador = pygame.Rect(POSICION_ORIGEN, h - 100, 32, 48)
bala_horizontal = pygame.Rect(w - 50, h - 90, 16, 16)
bala_vertical = pygame.Rect(30 + 24, 60, 16, 16)
nave_superior = pygame.Rect(30, 20, 64, 64)
nave = pygame.Rect(w - 100, h - 100, 64, 64)

# --- VELOCIDADES ---
velocidad_bala = -50
velocidad_bala_vertical = 3
bala_disparada = False

# --- ANIMACIÓN ---
current_frame = 0
frame_speed = 10
frame_count = 0

# --- FONDO ---
fondo_x1 = 0
fondo_x2 = w

# --- FUENTES ---
fuente = pygame.font.SysFont('Arial', 24)
fuente_grande = pygame.font.SysFont('Consolas', 56)

# --- RECURSOS VISUALES ---
jugador_frames = [
    pygame.image.load('assets/sprites/mono_frame_1.png'),
    pygame.image.load('assets/sprites/mono_frame_2.png'),
    pygame.image.load('assets/sprites/mono_frame_3.png'),
    pygame.image.load('assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/fondo2.png')
nave_img = pygame.image.load('assets/game/ufo.png')
menu_img = pygame.image.load('assets/game/menu.png')
fondo_img = pygame.transform.scale(fondo_img, (w, h))


def disparar_bala_horizontal():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -4)
        bala_disparada = True

def reset_bala_horizontal():
    global bala_disparada
    bala_horizontal.x = w - 50
    bala_disparada = False

def reset_bala_vertical():
    bala_vertical.x = 30 + 24
    bala_vertical.y = nave_superior.bottom

def manejar_salto():
    global salto, salto_altura, en_suelo
    if salto:
        jugador.y -= salto_altura
        salto_altura -= gravedad
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15
            en_suelo = True

def entrenar_modelos():
    global modelo_salto_arbol, modelo_movimiento_arbol
    global modelo_salto_nn, modelo_movimiento_nn
    global modelo_salto_knn, modelo_movimiento_knn

    if datos_salto:
        X = [(v, d) for v, d, s in datos_salto]
        y = [s for v, d, s in datos_salto]
        modelo_salto_arbol = DecisionTreeClassifier().fit(X, y)
        modelo_salto_nn = MLPClassifier(max_iter=500).fit(X, y)
        modelo_salto_knn = KNeighborsClassifier(n_neighbors=3).fit(X, y)
        print(f"\nModelos salto entrenados con {len(X)} muestras.")
    else:
        modelo_salto_arbol = None
        modelo_salto_nn = None
        modelo_salto_knn = None

    if datos_movimiento:
        X_mov = [[dx, jug_x, bala_x] for (dx, jug_x, bala_x), accion in datos_movimiento]
        y_mov = [accion for (_, _, _), accion in datos_movimiento]
        modelo_movimiento_arbol = DecisionTreeClassifier().fit(X_mov, y_mov)
        modelo_movimiento_nn = MLPClassifier(max_iter=500).fit(X_mov, y_mov)
        modelo_movimiento_knn = KNeighborsClassifier(n_neighbors=3).fit(X_mov, y_mov)
        print(f"Modelos movimiento entrenados con {len(X_mov)} muestras.")
    else:
        modelo_movimiento_arbol = None
        modelo_movimiento_nn = None
        modelo_movimiento_knn = None

def mostrar_datos_guardados():
    print("\n--- DATOS DE SALTO ---")
    for d in datos_salto:
        print(d)
    print("--- DATOS DE MOVIMIENTO ---")
    for d in datos_movimiento:
        print(d)

def prediccion_salto():
    if modo_modelo == 'arbol' and modelo_salto_arbol:
        dx = abs(jugador.x - bala_horizontal.x)
        return modelo_salto_arbol.predict([(velocidad_bala, dx)])[0] == 1
    elif modo_modelo == 'nn' and modelo_salto_nn:
        dx = abs(jugador.x - bala_horizontal.x)
        return modelo_salto_nn.predict([(velocidad_bala, dx)])[0] == 1
    elif modo_modelo == 'knn' and modelo_salto_knn:
        dx = abs(jugador.x - bala_horizontal.x)
        return modelo_salto_knn.predict([(velocidad_bala, dx)])[0] == 1
    return False

def prediccion_movimiento():
    if modo_modelo == 'arbol' and modelo_movimiento_arbol:
        dx = abs(jugador.x - bala_vertical.x)
        return modelo_movimiento_arbol.predict([[dx, jugador.x, bala_vertical.x]])[0]
    elif modo_modelo == 'nn' and modelo_movimiento_nn:
        dx = abs(jugador.x - bala_vertical.x)
        return modelo_movimiento_nn.predict([[dx, jugador.x, bala_vertical.x]])[0]
    elif modo_modelo == 'knn' and modelo_movimiento_knn:
        dx = abs(jugador.x - bala_vertical.x)
        return modelo_movimiento_knn.predict([[dx, jugador.x, bala_vertical.x]])[0]
    return 0

def guardar_datos_salto():
    dx = abs(jugador.x - bala_horizontal.x)
    salto_hecho = 1 if salto else 0
    datos_salto.append((velocidad_bala, dx, salto_hecho))

def guardar_datos_movimiento(accion):
    dx = abs(jugador.x - bala_vertical.x)
    datos_movimiento.append(((dx, jugador.x, bala_vertical.x), accion))

def mostrar_menu():
    global menu_activo, modo_auto, modo_modelo
    pantalla.blit(fondo_img, (0, 0))
    overlay = pygame.Surface((w, h))
    overlay.set_alpha(190)
    overlay.fill((30, 30, 30))
    pantalla.blit(overlay, (0, 0))

    # Define las líneas del menú
    lineas = [
        "MODOS:",
        "{M} Manual ",
        "{R} RW",
        "{D} DT ",
        "{K} KNN",
        "{G} Guardar",
        "{E} Entrenar",
        "--------------",
        "{S} Salir "
    ]

    fuente_titulo = pygame.font.SysFont('Consolas', 48)
    fuente_opcion = pygame.font.SysFont('Consolas', 28)

    # Calcula el alto total del menú
    alto_total = fuente_titulo.get_height() + (len(lineas) - 1) * fuente_opcion.get_height() + 15 * (len(lineas) - 1)
    y_inicio = h // 2 - alto_total // 2

    # Dibuja cada línea centrada
    for idx, linea in enumerate(lineas):
        if idx == 0:
            texto = fuente_titulo.render(linea, True, BLANCO)
        else:
            texto = fuente_opcion.render(linea, True, BLANCO)
        x = w // 2 - texto.get_width() // 2
        y = y_inicio + idx * (fuente_opcion.get_height() + 15)
        pantalla.blit(texto, (x, y))

    pygame.display.flip()
    while menu_activo:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_m:
                    modo_auto = False
                    modo_modelo = None
                    datos_salto.clear()
                    datos_movimiento.clear()
                    menu_activo = False
                elif e.key == pygame.K_d:
                    modo_auto = True
                    modo_modelo = 'arbol'
                    menu_activo = False
                elif e.key == pygame.K_n or e.key == pygame.K_r:
                    modo_auto = True
                    modo_modelo = 'nn'
                    menu_activo = False
                elif e.key == pygame.K_k:
                    modo_auto = True
                    modo_modelo = 'knn'
                    menu_activo = False
                elif e.key == pygame.K_g:
                    mostrar_datos_guardados()
                elif e.key == pygame.K_e:
                    entrenar_modelos()
                    print("Modelos entrenados manualmente.")
                elif e.key == pygame.K_s:
                    pygame.quit()
                    exit()

def mostrar_colision():
    pantalla.fill(ROJO)
    texto = fuente_grande.render("Fin de juego", True, BLANCO)
    pantalla.blit(texto, (w // 2 - texto.get_width() // 2, h // 2 - texto.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(1500)  # 1.5 segundos

def reiniciar_juego():
    global salto, en_suelo, bala_disparada, menu_activo, fondo_x1, fondo_x2, accion_actual, tiempo_accion
    mostrar_colision()
    jugador.x, jugador.y = POSICION_ORIGEN, h - 100
    reset_bala_horizontal()
    reset_bala_vertical()
    salto = False
    en_suelo = True
    bala_disparada = False
    fondo_x1 = 0
    fondo_x2 = w
    accion_actual = 0
    tiempo_accion = 0
    menu_activo = True
    mostrar_menu()

def update():
    global current_frame, frame_count, fondo_x1, fondo_x2

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
    pantalla.blit(nave_img, (nave_superior.x, nave_superior.y))

    if bala_disparada:
        bala_horizontal.x += velocidad_bala
        if bala_horizontal.x < 0:
            reset_bala_horizontal()

    bala_vertical.y += velocidad_bala_vertical
    if bala_vertical.y > h:
        reset_bala_vertical()

    pantalla.blit(bala_img, (bala_horizontal.x, bala_horizontal.y))
    pantalla.blit(bala_img, (bala_vertical.x, bala_vertical.y))

    if jugador.colliderect(bala_horizontal) or jugador.colliderect(bala_vertical):
        print("Colisión con bala detectada")
        reiniciar_juego()

def main():
    global salto, en_suelo, accion_actual, tiempo_accion
    reloj = pygame.time.Clock()
    mostrar_menu()
    correr = True
    reset_bala_horizontal()
    reset_bala_vertical()

    while correr:
        movimiento = 0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE and en_suelo:
                salto = True
                en_suelo = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            jugador.x = max(0, jugador.x - 5)
            movimiento = 1
        elif keys[pygame.K_RIGHT]:
            jugador.x = min(w - jugador.width, jugador.x + 5)
            movimiento = 2
        else:
            movimiento = 0

        if salto:
            manejar_salto()

        destino = bala_vertical.x - jugador.width // 2
        regresar_caminando = (
            bala_vertical.y > jugador.y + jugador.height and
            abs(jugador.x - destino) > 3
        )

        if modo_auto:
            if en_suelo and prediccion_salto():
                salto = True
                en_suelo = False

            if regresar_caminando:
                if jugador.x < destino:
                    jugador.x += 6
                elif jugador.x > destino:
                    jugador.x -= 6
            else:
                mov_pred = prediccion_movimiento()
                if mov_pred != accion_actual:
                    if tiempo_accion >= UMBRAL_TIEMPO:
                        accion_actual = mov_pred
                        tiempo_accion = 0
                    else:
                        tiempo_accion += 1
                else:
                    tiempo_accion = 0

                dx = bala_vertical.x - jugador.x
                if accion_actual == 1 and jugador.x > 0 and abs(dx) < UMBRAL_PELIGRO:
                    jugador.x -= 5
                elif accion_actual == 2 and jugador.x < w - jugador.width and abs(dx) < UMBRAL_PELIGRO:
                    jugador.x += 5
        else:
            if regresar_caminando:
                if jugador.x < destino:
                    jugador.x += 6
                elif jugador.x > destino:
                    jugador.x -= 6
            else:
                guardar_datos_salto()
                if movimiento != 0:
                    guardar_datos_movimiento(movimiento)

        if not bala_disparada:
            disparar_bala_horizontal()

        update()
        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
