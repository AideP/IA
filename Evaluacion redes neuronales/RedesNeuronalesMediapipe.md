# Evaluación: Redes Neuronales Mediapipe
### Nombre: Aide Pérez Andrade Numero de control: 21120246

### **Instrucciones:  **
    Modelar una red neuronal que pueda identificar emociones a través de los valores obtenidos de los landmarks que genera mediapipe.

    - Definir el tipo de red neuronal y describir cada una de sus partes.
    - Definir los patrones a utilizar.
    - Definir función de activación es necesaria para ese problema.
    - Definir el número máximo de entradas.
    - ¿Qué valores a la salida de la red se podrían esperar?
    - ¿Cuáles son los valores máximos que puede tener el bias?

### **-------------------------------------------------------------------------------------------------------------------------------  **
## **Respuestas  **
### 1. Tipo de Red Neuronal y Descripción de sus Partes
MediaPipe Face Mesh proporciona **468 puntos 3D** (coordenadas x, y, z) por lo tanto creo que seria conveniente utilizar

### Red Neuronal Densa (Fully Connected)
- **Capa de Entrada:** recibe todos los datos de los landmarks (468 x 3 = 1404 entradas).
- **Capas Ocultas:** múltiples capas densas que permiten detectar patrones complejos (se utiliza la función de activación ReLU)
- **Capa de Salida:** contiene una neurona por cada emoción, con activación *softmax* para clasificar en una sola categoría.

-----------------------------------------------------------------------------------------------------------------------------------------

### 2. Patrones a Utilizar
Los patrones que se pueden usar como entrada para la red incluyen:
- La posición y movimiento de cejas, ojos y boca.
- La distancia relativa entre puntos clave (ojos, nariz, boca).
- Cambios geométricos del rostro asociados a expresiones.

-----------------------------------------------------------------------------------------------------------------------------------------

### 3. Funciones de Activación
- **ReLU (Rectified Linear Unit):** para las capas ocultas, ya que es eficiente computacionalmente y evita el problema del desvanecimiento del gradiente.
- **Softmax:** en la capa de salida para obtener una probabilidad por cada emoción y realizar clasificación multiclase.

-----------------------------------------------------------------------------------------------------------------------------------------

### 4. Número Máximo de Entradas
- Si se usan los **468 puntos** teniendo en cuenta sus 3 coordenadas (x,y,z)
  - `468 × 3 = 1404 entradas`

-----------------------------------------------------------------------------------------------------------------------------------------

### 5. Valores Esperados a la Salida de la Red
- La red devuelve un vector de probabilidades, por ejemplo:
```python
[0.10, 0.05, 0.60, 0.05, 0.10, 0.10]
```
- Cada valor representa la probabilidad de una emoción: alegría, tristeza, enojo, sorpresa, miedo y neutral.
- Se espera que la **suma de todos los valores sea 1.0** (propiedad de softmax).

-----------------------------------------------------------------------------------------------------------------------------------------
ss
### 6. Valores Máximos del Bias
- **No existe un valor máximo definido** para el bias.
- El bias es un valor **aprendido** durante el entrenamiento de la red.
- Puede tomar valores positivos o negativos dependiendo del problema.
- Por lo general, se inicializa en cero o con valores pequeños; por lo tanto actualmente no puedo decir el valor máximo del bias.


