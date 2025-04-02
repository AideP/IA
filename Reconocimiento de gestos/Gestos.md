# Reconocimiento de vida a través de gestos utilizando mediapipe

A través de mediapipe podemos hacer uso de landmarks que nos ayudarán a reconocer ciertos datos
especificos de una persona, podriamos utilizarla para detectar rostros, asi mismo mediapipe tiene un desarrollo
llamado mediapipe hands que nos permite reconocer las landmarks que existen en las manos asi como lograr identificar
entre la mano izquierda y derecha, lo que deseamos lograr con este proyecto es llegar al desarrollo de un programa que
nos permita detectar si la persona que tenemos frente a la cámara esta viva o es una imagen, esto a través de la detección
de gestos que realiza una persona viva, como lo podría ser un ceño fruncido demostrando enojo, una sonrisa demostrando tristeza, etc.

### ¿Qué se necesita para detectar si una persona esta viva?
En un inicio debemos tener en cuenta que una persona viva realiza varios movimientos "gestos" como pueden ser el movimiento ocular, etc.
necesitamos tener identificados los puntos clave de la cara (face landmarks),
debemos tener en cuenta los movimientos que puede realizar una persona como el movimiento ocular, parpadeo (movimiento entre fotogramas),
asi como debemos tener en cuenta la distancia que existe entre las marcas mas importantes de un rostro como lo son las cejas, los ojos, boca y nariz.

### ¿Qué utilizar?
Mediapipe aparte de tener desarrollado mediapipe hands para la detección de manos y dedos tiene desarrollado mediapipe FaceDetection y mediaPipe Face Mesh que nos ayudarán a la detección de landmarks en el rostro, mediapipe Face Mesh nos da la oportunidad de utilizar **468 puntos** clave que se encuentran en la cara, estos puntos se encuentran en formato 3D