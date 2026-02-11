# ------------------------------------------------------------
# Boletines Judiciales System (BJS)
#
# Desarrollado por: Daniel Ionut C.
# Marca / iniciativa: Ionut IT
# Fecha: Febrero 2026
#
# Licencia pública con restricción comercial.
# Antes de usar, modificar o redistribuir este código:
# - Lea el archivo LICENSE
# - Lea el archivo README.md
#
# Uso personal permitido.
# Uso comercial o implementación a terceros requiere licencia.
#
# Este software se ofrece "AS IS", sin garantías de ningún tipo.
#
# Desarrollado con ♥ por Ionut IT
# ------------------------------------------------------------

import os
import json
import mysql.connector
import fitz  # PyMuPDF
import re
from llama_cpp import Llama

# Configuration
DB_CONFIG = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'bjs_db'
}

MODEL_DIR = r"C:\xampp\htdocs\BJS\modelos"

class Processor:
    def __init__(self):
        self.llm = None
        self.load_model()

    def load_model(self):
        """Loads the first .gguf model found in the models directory."""
        if not os.path.exists(MODEL_DIR):
            print(f"Model directory not found: {MODEL_DIR}")
            return

        models = [f for f in os.listdir(MODEL_DIR) if f.endswith(".gguf")]
        if not models:
            print(f"No .gguf models found in {MODEL_DIR}. Please add a model file.")
            return

        model_path = os.path.join(MODEL_DIR, models[0])
        print(f"Loading model: {model_path}...")
        try:
            # Context size is critical. A standard model handles 2048 or 4096.
            # We must be careful not to overflow.
            self.llm = Llama(model_path=model_path, n_ctx=4096, verbose=False)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Failed to load model: {e}")

    def extract_text_from_pdf(self, pdf_path):
        """Extracts text from PDF using PyMuPDF."""
        try:
            print(f"Attempting to extract text from {pdf_path} using PyMuPDF")
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            
            print(f"Raw text length: {len(text)}")
            return text
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return ""

    def analyze_chunk(self, chunk, force_found=False):
        """Analyzes a single chunk of text with Llama.cpp."""
        if not self.llm:
            print("Model not loaded. Cannot analyze.")
            return None

        # Clean chunk
        clean_chunk = chunk.replace('"', "'").replace('\n', ' ')
        
        # Add force hint to prompt
        force_instruction = ""
        if force_found:
            force_instruction = "IMPORTANTE: Este texto COMIENZA con 'En este Despacho', por lo que ES un remate. Debes responder con found: true AUNQUE falten datos."

        prompt = f"""<|im_start|>system
Eres un asistente legal experto en Costa Rica. Tu única tarea es extraer datos de remates judiciales en formato JSON.
<|im_end|>
<|im_start|>user
Analiza el siguiente texto y extrae UN remate judicial de VEHÍCULO o PROPIEDAD.
{force_instruction}

Texto:
{clean_chunk}

Responde SOLO con un JSON válido con este formato exacto:
{{
    "found": true,
    "tipo": "vehiculo" | "propiedad" | "desconocido",
    "descripcion": "breve descripción del bien",
    "marca": "marca o null",
    "modelo": "modelo o null",
    "vin": "VIN o chasis o null",
    "placa": "placa o matrícula o null",
    "precio_base": "monto o null",
    "ubicacion": "provincia o lugar o null",
    "juzgado": "nombre del despacho o null",
    "fecha_remate": "fecha y hora o null"
}}

Si realmente NO hay información de remate, responde: {{ "found": false }}
<|im_end|>
<|im_start|>assistant
"""

        try:
            output = self.llm(
                prompt, 
                max_tokens=500, 
                stop=["<|im_end|>", "<|im_start|>"], 
                echo=False,
                temperature=0.1
            )
            response_text = output['choices'][0]['text']
            
            # Simple JSON extraction regex
            json_match = re.search(r'\{.*\}', response_text.replace('\n', ''), re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                # Enforce found=True if forced
                if force_found and not data.get('found'):
                    print("Force found: Overriding found=False from LLM.")
                    data['found'] = True
                    if not data.get('descripcion'):
                        data['descripcion'] = "Remate detectado (Extracción incompleta)"
                return data
            
            if force_found:
                 print("Force found: JSON parsing failed, returning generic found object.")
                 return {
                     "found": True, 
                     "tipo": "desconocido", 
                     "descripcion": "Error al extraer datos, pero remate detectado.",
                     "texto_completo": clean_chunk[:200]
                 }
                 
            return None
        except Exception as e:
            print(f"Error in LLM inference: {e}")
            if force_found:
                 return {
                     "found": True, 
                     "tipo": "desconocido", 
                     "descripcion": "Error técnico, registro forzado."
                 }
            return None

    def save_to_db(self, data, raw_text):
        """Inserts extracted data into MySQL."""
        if not data:
            return False
            
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            sql = """
            INSERT INTO remates 
            (tipo, descripcion, marca, modelo, vin, placa, matricula, precio_base, ubicacion, juzgado, fecha_remate, texto_completo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            vals = (
                data.get('tipo'),
                data.get('descripcion'),
                data.get('marca'),
                data.get('modelo'),
                data.get('vin'),
                data.get('placa'),
                data.get('matricula'),
                data.get('precio_base'),
                data.get('ubicacion'),
                data.get('juzgado'),
                data.get('fecha_remate'),
                raw_text[:1000] # Store snippet or full text depending on preference
            )
            
            cursor.execute(sql, vals)
            conn.commit()
            cursor.close()
            conn.close()
            print("Data saved to database.")
            return True
        except Exception as e:
            print(f"Database error: {e}")
            return False

    def process_file(self, file_path):
        print(f"Processing {file_path}...")
        try:
            text = self.extract_text_from_pdf(file_path)
            if not text:
                print("No text extracted.")
                return
            
            # Smart Chunking: Look for "En este Despacho" phrase
            # User specified: "casi todos los remates empiezan con : En este Despacho"
            # We look for this phrase (case-insensitive just in case)
            phrase = "En este Despacho"
            keyword_indices = [m.start() for m in re.finditer(re.escape(phrase), text, re.IGNORECASE)]
            high_confidence = True
            
            if not keyword_indices:
                print(f"No '{phrase}' phrases found in text. Falling back to 'remate' keyword.")
                keyword_indices = [m.start() for m in re.finditer(r'(?i)remate', text)]
                high_confidence = False
                
            if not keyword_indices:
                print("No suitable keywords found in text.")
                return

            print(f"Found {len(keyword_indices)} potential auctions. High confidence: {high_confidence}")
            
            # Process all occurrences
            for i, idx in enumerate(keyword_indices):
                # Start slightly before to capture context if needed, but mainly after
                start = idx
                end = min(len(text), idx + 3000) # Capture a good chunk of text
                chunk = text[start:end]
                
                print(f"Comparing chunk {i+1}...")
                data = self.analyze_chunk(chunk, force_found=high_confidence)
                
                if data and data.get('found'):
                    print(f"Match found in chunk {i+1}: {data}")
                    self.save_to_db(data, chunk) # Save the relevant chunk text
                else:
                    print(f"No data in chunk {i+1}")
                    
        except Exception as e:
            print(f"CRITICAL ERROR in process_file: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    # Test run
    proc = Processor()
    # proc.process_file(r"C:\xampp\htdocs\BJS\PDF\Boletín Judicial N° 026-2026 .pdf")
