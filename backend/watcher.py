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

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backend.processor import Processor

PDF_DIR = r"C:\xampp\htdocs\BJS\PDF"

class PDFHandler(FileSystemEventHandler):
    def __init__(self):
        self.processor = Processor()

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith('.pdf'):
            print(f"New PDF detected: {event.src_path}")
            # Wait a bit for file copy to complete
            time.sleep(1) 
            self.processor.process_file(event.src_path)

if __name__ == "__main__":
    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR)
        
    event_handler = PDFHandler()
    observer = Observer()
    observer.schedule(event_handler, PDF_DIR, recursive=False)
    observer.start()
    print(f"Watching for PDFs in {PDF_DIR}...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
