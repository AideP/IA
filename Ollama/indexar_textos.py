import os
import requests
from chromadb import PersistentClient
import time

# Configuración
carpetas = {
    "aborto": "ollama/aborto/texto_pdf",
    "eutanasia": "ollama/eutanasia/texto_pdf"
}

client = PersistentClient(path="db_ollama")
collection = client.get_or_create_collection("ollama_textos")
modelo_embeddings = "nomic-embed-text:latest"

def verificar_modelo():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        models = [m["name"] for m in response.json()["models"]]
        return modelo_embeddings in models
    except:
        return False

def generar_embedding(texto, intentos=3):
    for _ in range(intentos):
        try:
            response = requests.post(
                "http://localhost:11434/api/embeddings",
                json={
                    "model": modelo_embeddings,
                    "prompt": texto[:10000]  
                },
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()
                print("🔎 Respuesta cruda:", data) 
                embedding = data.get("embedding")
                if embedding and len(embedding) > 0:
                    return embedding
                else:
                    print("⚠️ Embedding vacío en la respuesta")
            else:
                print(f"❌ Error HTTP {response.status_code}: {response.text}")

        except Exception as e:
            print(f"🔴 Excepción al generar embedding: {str(e)}")

        time.sleep(2)

    return None

if not verificar_modelo():
    print(f"🚨 Modelo '{modelo_embeddings}' no disponible en Ollama!")
    print("Ejecuta: ollama pull nomic-embed-text")
    exit(1)

for tema, carpeta in carpetas.items():
    if not os.path.exists(carpeta):
        print(f"📂 Carpeta no encontrada: {carpeta}")
        continue

    for archivo in os.listdir(carpeta):
        if not archivo.endswith(".txt"):
            continue

        ruta = os.path.join(carpeta, archivo)
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                texto = f.read().strip()

            if not texto:
                print(f"📄 Archivo vacío: {archivo}")
                continue

            print(f"🔍 Procesando: {archivo}...")
            embedding = generar_embedding(texto)

            if embedding:
                doc_id = f"{tema}_{archivo}"
                collection.add(
                    documents=[texto],
                    embeddings=[embedding],
                    ids=[doc_id],
                    metadatas=[{"tema": tema, "archivo": archivo}]
                )
                print(f"✅ Indexado: {doc_id}")
            else:
                print(f"❌ Falló embedding para: {archivo}")

        except Exception as e:
            print(f"🔥 Error crítico en {archivo}: {str(e)}")

print("🎉 Proceso finalizado!")
