import cv2
import mediapipe as mp
import numpy as np
import json

# Inicializar MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False, max_num_faces=2,
    min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Captura de video
cap = cv2.VideoCapture(0)

# Puntos específicos: ojos y boca
selected_points = [33, 133, 362, 263, 61, 291]

# Lista donde guardaremos los datos de todas las personas registradas
personas_guardadas = []

def distancia(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    frame_personas = []  # Lista de personas en este frame

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            puntos = {}
            for idx in selected_points:
                x = int(face_landmarks.landmark[idx].x * frame.shape[1])
                y = int(face_landmarks.landmark[idx].y * frame.shape[0])
                puntos[str(idx)] = {'x': x, 'y': y}
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Mostrar líneas y distancias en la imagen
            if '33' in puntos and '133' in puntos:
                p1, p2 = (puntos['33']['x'], puntos['33']['y']), (puntos['133']['x'], puntos['133']['y'])
                d = distancia(p1, p2)
                cv2.line(frame, p1, p2, (0, 255, 0), 2)
                cv2.putText(frame, f"Ojo Izq: {int(d)}px", (p1[0], p1[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            if '362' in puntos and '263' in puntos:
                p1, p2 = (puntos['362']['x'], puntos['362']['y']), (puntos['263']['x'], puntos['263']['y'])
                d = distancia(p1, p2)
                cv2.line(frame, p1, p2, (0, 200, 255), 2)
                cv2.putText(frame, f"Ojo Der: {int(d)}px", (p1[0], p1[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1)

            if '61' in puntos and '291' in puntos:
                p1, p2 = (puntos['61']['x'], puntos['61']['y']), (puntos['291']['x'], puntos['291']['y'])
                d = distancia(p1, p2)
                cv2.line(frame, p1, p2, (255, 0, 0), 2)
                cv2.putText(frame, f"Boca: {int(d)}px", (p1[0], p1[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

            # Guardar los puntos de esta persona
            frame_personas.append(puntos)

    # Mostrar cámara
    cv2.imshow('PuntosFacialesMediaPipe', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('a'):
        break
    elif key == ord('s'):
        if frame_personas:
            print(f"Guardando {len(frame_personas)} persona(s)...")
            for persona in frame_personas:
                personas_guardadas.append(persona)
        else:
            print("No hay rostros para guardar.")

# Guardar archivo JSON al final
if personas_guardadas:
    with open("cara_guarda.json", "w") as f:
        json.dump(personas_guardadas, f, indent=4)
    print("Archivo 'cara_guarda.json' generado con éxito.")

cap.release()
cv2.destroyAllWindows()
