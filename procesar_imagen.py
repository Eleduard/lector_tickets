import tempfile

from fastapi import File, HTTPException, UploadFile
from ocr import ocr

ALLOWED_TYPES = {"image/jpeg", "application/pdf"}
MAX_SIZE_MB = 20
EXTENSIONES = {
    "image/jpeg": ".jpg",
    "application/pdf": ".pdf",
}

async def procesar_imagen(file: UploadFile) -> str:
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
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al realizar OCR: {str(e)}"
        )
    finally:
        if tmp_path:
            import os
            os.remove(tmp_path)

    return texto_ocr