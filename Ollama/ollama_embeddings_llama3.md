
# 🧠 Comprendiendo los Embeddings, Ollama y Llama 3.2

## 📌 ¿Qué son los *embeddings*?

Los **embeddings** son representaciones numéricas de textos en forma de vectores. Su función principal es traducir palabras, frases o documentos en números que conserven su significado semántico, permitiendo que una computadora compare similitudes entre textos.

Por ejemplo:
- *“aborto”* y *“interrupción del embarazo”* deberían tener vectores cercanos porque significan lo mismo.
- Esto permite realizar búsquedas semánticas, no solo por palabras exactas.

> En este proyecto usamos el modelo `nomic-embed-text` para generar estos embeddings usando Ollama localmente.

---

## ⚙️ ¿Cómo se generan y usan los embeddings en este sistema?

### 1. **Indexación de textos** (`indexar_textos.py`):
- Se leen archivos `.txt` desde carpetas temáticas (ej. `aborto`, `eutanasia`).
- Cada texto se envía a `http://localhost:11434/api/embeddings` usando el modelo `nomic-embed-text`.
- El vector de embedding devuelto se guarda en una base de datos local (`ChromaDB`) junto con el texto y metadatos.

### 2. **Consulta de información** (`preguntar.py`):
- El usuario escribe una pregunta.
- Esta pregunta se transforma también en un embedding.
- Se busca el vector más cercano dentro de los documentos ya indexados.
- Se seleccionan los textos más relevantes para armar un *contexto*.
- Ese contexto + pregunta se pasan como *prompt* a un modelo LLM (en este caso `llama3`).

---

## 🧠 ¿Qué es Ollama?

**Ollama** es una herramienta que permite ejecutar modelos de lenguaje grandes (*Large Language Models*) localmente, sin depender de la nube.

**Ventajas:**
- No necesitas conexión a OpenAI ni otras APIs externas.
- Puedes usar modelos como LLaMA, Mistral, Gemma, entre otros.
- Accedes a endpoints REST como `/api/generate` y `/api/embeddings`.

En este proyecto usamos Ollama para dos tareas:
- Generar *embeddings* (`/api/embeddings`)
- Generar respuestas (`/api/generate`)

---

## 🦙 ¿Qué es LLaMA 3.2 (llama3)?

**LLaMA** (Large Language Model Meta AI) es una familia de modelos de lenguaje desarrollada por **Meta (Facebook)**. En su versión 3.2, ofrece mejoras significativas en comprensión, velocidad y respuesta natural del lenguaje.

Características clave de `llama3.2`:
- Capacidad para trabajar localmente vía Ollama.
- Compatible con prompts de tipo *instrucción-respuesta*.
- Puede responder preguntas específicas usando contexto personalizado.

---

## 🧪 Flujo general del sistema

```
Usuario (Pregunta) ──▶ [Generar embedding de la pregunta]
                              │
                              ▼
                 [Buscar documentos similares en ChromaDB]
                              │
                              ▼
                [Construir contexto + pregunta como prompt]
                              │
                              ▼
                     [Enviar a llama3 via Ollama]
                              │
                              ▼
                        🧠 Respuesta generada
```

---

## 📁 Estructura de archivos

```
IA/
│
├── indexar_textos.py    # Indexa textos con embeddings
├── preguntar.py         # Permite hacer preguntas al modelo
├── db_ollama/           # Base de datos local de Chroma (persistente)
├── ollama/              # Carpeta con textos por tema
│   ├── aborto/texto_pdf/*.txt
│   └── eutanasia/texto_pdf/*.txt

```

---

## ✅ Requisitos

- Tener instalado **Ollama**: [https://ollama.com](https://ollama.com)
- Modelos necesarios:
  ```bash
  ollama pull nomic-embed-text
  ollama pull llama3
  ```
- Tener ChromaDB y `requests` instalados:
  ```bash
  pip install chromadb requests
  ```

---

## 🔄 Comandos de ejecución

**Para indexar textos:**
```bash
python indexar_textos.py
```

**Para hacer preguntas:**
```bash
python preguntar.py
```

---

## 🧩 Posibles errores y soluciones

| Problema                           | Solución recomendada                                           |
|------------------------------------|----------------------------------------------------------------|
| `list index out of range` en query | Asegúrate de que se generen correctamente los embeddings.      |
| Embeddings vacíos                  | Verifica que `nomic-embed-text` esté funcionando en Ollama.    |
| No se encuentra modelo             | Ejecuta `ollama pull nomic-embed-text` o `llama3`              |
| Archivos `.txt` vacíos             | Asegúrate de que los textos tengan contenido relevante.        |
