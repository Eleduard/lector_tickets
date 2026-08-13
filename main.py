import tempfile

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ocr import ocr
from groq_a_json import crear_json

from procesar_imagen import procesar_imagen

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5173/"],
    allow_methods=["POST"],
    allow_headers=["*"]
)

@app.post("/ocr")
async def root(file: UploadFile = File(...)):
    
    # Procesar la imagen y obtener el texto OCR
    texto_ocr = await procesar_imagen(file)

    # Enviar el texto OCR a la función de Groq para obtener el JSON estructurado
    resultado_json = await crear_json(texto_ocr)
    
    # Imprimir el resultado final
    # print(json.dumps(resultado_json, indent=4))
    return resultado_json
