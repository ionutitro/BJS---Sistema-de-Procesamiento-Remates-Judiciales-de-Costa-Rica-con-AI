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

import sys
import os

# Add the parent directory to sys.path to allow imports if running from backend/
# But if we run from root, we need to handle imports carefully.
# Let's assume we run this from c:\xampp\htdocs\BJS

sys.path.append(os.path.join(os.getcwd()))

from backend.processor import Processor

def test_pipeline():
    print("Initializing Processor...")
    try:
        proc = Processor()
    except Exception as e:
        print(f"Failed to initialize Processor: {e}")
        return

    if not proc.llm:
        print("LLM not loaded.")
        return
    else:
        print("LLM loaded successfully.")

    pdf_path = r"C:\xampp\htdocs\BJS\PDF\Boletín Judicial N° 026-2026 .pdf"
    if not os.path.exists(pdf_path):
        print(f"PDF not found at {pdf_path}")
        return

    print(f"Processing {pdf_path}...")
    proc.process_file(pdf_path)

if __name__ == "__main__":
    test_pipeline()
