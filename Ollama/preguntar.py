import requests
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
import time

# Configura Ollama y ChromaDB
OLLAMA_HOST = "http://localhost:11434"
CHROMA_DB_PATH = "db_ollama"

# Inicialización mejorada
client = PersistentClient(path=CHROMA_DB_PATH)

# Usa el modelo correcto para embeddings (compatible con Llama 3.2)
embedding_func = embedding_functions.OllamaEmbeddingFunction(
    url=f"{OLLAMA_HOST}/api/embeddings",
    model_name="llama3:8b-instruct-q4_0"  # Modelo específico para embeddings
)

collection = client.get_or_create_collection(
    name="ollama_textos",
    embedding_function=embedding_func
)

def verificar_modelos():
    """Verifica que los modelos estén disponibles"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=10)
        modelos = [m["name"] for m in response.json().get("models", [])]
        
        modelos_requeridos = ["llama3:8b-instruct-q4_0", "llama3"]
        for modelo in modelos_requeridos:
            if modelo not in modelos:
                print(f"⚠️ Modelo faltante: {modelo}")
                print("Ejecuta: ollama pull llama3:8b-instruct-q4_0")
                return False
        return True
    except Exception as e:
        print(f"❌ Error conectando con Ollama: {str(e)}")
        return False

def generar_respuesta(prompt):
    """Generación de respuestas con manejo de errores mejorado"""
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_ctx": 4096  # Contexto ampliado
                }
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "No se obtuvo respuesta")
    except Exception as e:
        return f"Error al generar respuesta: {str(e)}"

def responder_pregunta(pregunta):
    try:
        # Paso 1: Generar embedding usando la función de la colección
        embedding_pregunta = embedding_func([pregunta])
        if not embedding_pregunta or len(embedding_pregunta[0]) == 0:
            return "❌ No se pudo generar embedding válido"
        
        # Paso 2: Consultar documentos relevantes
        resultados = collection.query(
            query_embeddings=embedding_pregunta,
            n_results=3,
            include=["documents", "distances", "metadatas"]
        )
        
        # Validación exhaustiva de resultados
        if not resultados["documents"] or not resultados["documents"][0]:
            return "⚠️ No se encontraron documentos relevantes"
        
        # Paso 3: Construir contexto
        contexto = "\n\n---\n\n".join([
            doc for doc in resultados["documents"][0] 
            if doc and doc.strip()
        ])
        
        if not contexto:
            return "⚠️ Los documentos recuperados están vacíos"
        
        # Paso 4: Generar prompt estructurado
        prompt = f"""Instrucción: Responde únicamente basándote en el contexto proporcionado.

Contexto:
{contexto}

Pregunta: {pregunta}

Respuesta:"""
        
        return generar_respuesta(prompt)
        
    except Exception as e:
        return f"❌ Error procesando pregunta: {str(e)}"

if __name__ == "__main__":
    print("🔍 Inicializando sistema...")
    
    if not verificar_modelos():
        exit(1)
    
    print("\n💬 Sistema de Q&A con Llama 3.2 (escribe 'salir' para terminar)")
    
    while True:
        try:
            pregunta = input("\n❓ Tu pregunta: ").strip()
            if pregunta.lower() in ('salir', 'exit', 'quit'):
                break
                
            inicio = time.time()
            respuesta = responder_pregunta(pregunta)
            tiempo = time.time() - inicio
            
            print(f"\n📝 Respuesta ({tiempo:.2f}s):")
            print(respuesta)
            
        except KeyboardInterrupt:
            print("\n👋 Sesión finalizada")
            break
        except Exception as e:
            print(f"\n⚠️ Error: {str(e)}")