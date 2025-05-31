# Juego de Esquivar Balas con Inteligencia Artificial (Pygame + Machine Learning)

Este proyecto es un juego desarrollado en **Python** usando **Pygame** y modelos de **Machine Learning** para crear un sistema interactivo en el que puedes jugar manualmente, entrenar a una IA con tus propios movimientos y luego dejar que la IA juegue por ti. El jugador debe esquivar balas que vienen de diferentes direcciones.

## 🎮 Características

- **Modo Manual:** Controla el personaje con el teclado para esquivar balas y saltar.
- **Modo Automático:** La IA, entrenada con tus propios datos, toma el control del jugador.
- **Entrenamiento en Vivo:** Los datos de tus movimientos y saltos se registran mientras juegas manualmente.
- **Modelos ML integrados:** Árbol de Decisión, Red Neuronal (MLPClassifier) y K-Nearest Neighbors (KNN).
- **Menú interactivo:** Selecciona modos y modelos con solo presionar una tecla.

---

## 🕹️ Controles

- **Flecha Izquierda / Derecha:** Mover al jugador lateralmente
- **Barra Espaciadora:** Saltar
- **G:** Mostrar en consola los datos guardados para entrenamiento
- **E:** Entrenar los modelos ML con los datos recolectados
- **M:** Modo manual
- **D:** Activar Árbol de Decisión automático
- **N/R:** Activar Red Neuronal automática
- **K:** Activar modo KNN automático
- **S:** Salir del juego

---

## 📋 Menú de Opciones

Al iniciar o tras perder, verás este menú:

    MODOS:
        {M} Manual 
        {R} RW
        {D} DT
        {K} KNN
        {G} Guardar
        {E} Entrenar
        --------------
        {S} Salir 


Selecciona la opción deseada presionando la tecla correspondiente.

---

## 🧠 ¿Cómo aprende la IA?

1. **Juega en modo manual** (`M`): tus acciones (saltos y movimientos) se guardan.
2. **Revisa los datos** (`G`): imprime los datos registrados en la consola.
3. **Entrena el modelo** (`E`): usa tus datos para ajustar los modelos de IA.
4. **Juega en modo automático** (`D`, `N`, `K`, `R`): la IA toma el control usando el modelo elegido.

---

## 📦 Requisitos e Instalación

1. **Python 3.x**  
2. Instalar dependencias:
    ```bash
    pip install pygame scikit-learn
    ```

3. **Estructura recomendada de archivos:**
    ```
    assets/
      └── sprites/
          ├── mono_frame_1.png
          ├── mono_frame_2.png
          ├── mono_frame_3.png
          └── mono_frame_4.png
      └── game/
          ├── fondo2.png
          ├── ufo.png
          └── menu.png
    main.py      # (El archivo del juego)
    ```

---

## 🛠️ Ejecución

1. Coloca las imágenes necesarias en las carpetas indicadas (`assets/sprites` y `assets/game`).
2. Ejecuta el juego:
    ```bash
    python main.py
    ```
3. Juega manualmente, registra tus movimientos, entrena el modelo y ¡deja que la IA te sorprenda!

---

## 💡 Explicación Técnica

- **Datos recolectados:**  
  - Para saltos: velocidad de la bala, distancia al jugador, si saltó (1) o no (0).
  - Para movimientos: diferencia de posición entre jugador y bala, posiciones absolutas y acción realizada.
- **Modelos:**  
  - Se entrenan solo si presionas `E`.
  - El modelo activo decide saltar/esquivar según las predicciones de IA.


---

## 📝 Notas

- Este juego es un ejemplo educativo para aprender sobre Pygame y ML en videojuegos.


