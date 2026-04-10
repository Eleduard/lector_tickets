from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def crear_json(texto_ocr: str) -> dict:

    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )

    with open("prompt.txt", "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()

    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": "Aquí está el texto del ticket: \n" + texto_ocr
            }
        ]
    )
    
    # Extraer el contenido del mensaje de respuesta
    json_response = respuesta.choices[0].message.content
    
    # Convertir la cadena JSON a un diccionario de Python
    try:
        data = json.loads(json_response)
        return data
    except json.JSONDecodeError as e:
        print("Error al decodificar JSON:", e)
        return None