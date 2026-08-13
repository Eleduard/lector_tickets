import base64
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ocr import ocr
from groq_a_json import crear_json
import json
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5173/"],
    allow_methods=["POST"],
    allow_headers=["*"]
)

ALLOWED_TYPES = {"image/jpeg", "application/pdf"}
MAX_SIZE_MB = 20
EXTENSIONES = {
    "image/jpeg": ".jpg",
    "application/pdf": ".pdf",
}

@app.post("/ocr")
async def root(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no soportado: {file.content_type}"
        )
    contenido = await file.read()
    if len(contenido) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"El archivo excede el tamaño máximo permitido de {MAX_SIZE_MB} MB"
        )

    # Guardar el archivo temporalmente
    extension = EXTENSIONES[file.content_type]
    tmp_path = None
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
            tmp_file.write(contenido)
            tmp_path = tmp_file.name

        # Realizar OCR en la imagen del ticket
        texto_ocr = await ocr(tmp_path)
    finally:
        if tmp_path:
            import os
            os.remove(tmp_path)

    # Enviar el texto OCR a la función de Groq para obtener el JSON estructurado
    resultado_json = await crear_json(texto_ocr)
    
    # Imprimir el resultado final
    # print(json.dumps(resultado_json, indent=4))
    return resultado_json
