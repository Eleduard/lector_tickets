from ocr import ocr
from groq_a_json import crear_json
import json
import asyncio

async def main():
    # Paso 1: Realizar OCR en la imagen del ticket
    texto_ocr = await ocr("images/Escáner - 2026-04-02 13_48_25.pdf")
    
    # Paso 2: Enviar el texto OCR a la función de Groq para obtener el JSON estructurado
    resultado_json = await crear_json(texto_ocr)
    
    # Imprimir el resultado final
    print(json.dumps(resultado_json, indent=4))

if __name__ == "__main__":
    asyncio.run(main())
