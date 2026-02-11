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

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import shutil
import os
from backend.processor import Processor

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'bjs_db'
}

PDF_DIR = r"C:\xampp\htdocs\BJS\PDF"

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Helper for background task
def process_pdf_background(file_path: str):
    proc = Processor()
    proc.process_file(file_path)

@app.get("/api/remates")
def list_remates(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM remates ORDER BY fecha_registro DESC LIMIT %s, %s", (skip, limit))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

@app.get("/api/remates/{remate_id}")
def get_remate(remate_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM remates WHERE id = %s", (remate_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        raise HTTPException(status_code=404, detail="Remate not found")
    return result

@app.delete("/api/remates/{remate_id}")
def delete_remate(remate_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if exists first
    cursor.execute("SELECT id FROM remates WHERE id = %s", (remate_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Remate not found")
        
    cursor.execute("DELETE FROM remates WHERE id = %s", (remate_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Remate deleted successfully"}

@app.post("/api/upload")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR)
    
    file_path = os.path.join(PDF_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Trigger processing in background
    background_tasks.add_task(process_pdf_background, file_path)
    
    return {"filename": file.filename, "status": "Uploaded. Processing started in background."}

@app.get("/")
def read_root():
    return {"message": "BJS API is running"}
