
### **Modelado de una Red Neuronal para 5 en Línea sin gravedad en un Tablero 20x20**

### **-Definir el tipo de red neuronal y describir cada una de sus partes.**
### **-Definir los patrones a utilizar.**
### **-Definir función de activación es necesaria para este problema.**
### **-Definir el número máximo de entradas.**
### **-¿Qué valores a la salida de la red se podrían esperar?**
### **-¿Cuáles son los valores máximos que puede tener el bias?**


#### **1. Tipo de Red Neuronal y sus Partes**
Para este problema, se recomienda una **red neuronal profunda (Deep Neural Network - DNN)** o una **Red Neuronal Convolucional (CNN)** si se busca mejorar la interpretación espacial del tablero.  
Las partes principales de la red incluyen:
- **Capa de entrada:** Recibe el estado actual del tablero (20x20 casillas).
- **Capas ocultas:** Procesan la información mediante convoluciones (en caso de CNN) o transformaciones no lineales en una DNN.
- **Capa de salida:** Predice la mejor jugada en el tablero.

#### **2. Patrones a Utilizar**
Los patrones a considerar en la entrada de la red incluyen:
- **Distribución de fichas propias y del oponente** en el tablero.
- **Estados ganadores o críticos**, como cuatro fichas en línea con una casilla libre adyacente.
- **Bloqueo del oponente**, detectando si el adversario está cerca de ganar.

#### **3. Función de Activación**


