import os
from PyPDF2 import PdfReader

# Carpetas base y sus subcarpetas
temas = {
    'aborto': {
        'pdf': 'Ollama/aborto/pdfs',
        'txt': 'Ollama/aborto/texto_pdf'
    },
    'eutanasia': {
        'pdf': 'Ollama/eutanasia/pdfs',
        'txt': 'Ollama/eutanasia/texto_pdf'
    }
}

for tema, rutas in temas.items():
    ruta_pdf = rutas['pdf']
    ruta_txt = rutas['txt']
    
    # Crear carpeta destino si no existe
    os.makedirs(ruta_txt, exist_ok=True)
    
    # Procesar cada archivo PDF
    for archivo in os.listdir(ruta_pdf):
        if archivo.endswith('.pdf'):
            ruta_pdf_completa = os.path.join(ruta_pdf, archivo)
            ruta_txt_completa = os.path.join(ruta_txt, archivo.replace('.pdf', '.txt'))
            
            try:
                reader = PdfReader(ruta_pdf_completa)
                texto_completo = ''
                
                for pagina in reader.pages:
                    texto = pagina.extract_text()
                    if texto:
                        texto_completo += texto + '\n'
                
                with open(ruta_txt_completa, 'w', encoding='utf-8') as f:
                    f.write(texto_completo)
                
                print(f"✅ Convertido: {archivo} -> {ruta_txt_completa}")
            except Exception as e:
                print(f"❌ Error procesando {archivo}: {e}")

print("🚀 Todos los archivos PDF fueron convertidos a TXT con éxito.")
