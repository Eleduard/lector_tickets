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
    
    # Extraer el contenido del mensaje de respuesta y limpiar el JSON si es necesario
    json_response = respuesta.choices[0].message.content
    print("Respuesta de Groq:", json_response)

    if isinstance(json_response, str):
        primerLlave = json_response.find('{')
        ultimaLlave = json_response.rfind('}')

        if primerLlave != -1 and ultimaLlave != -1 and ultimaLlave > primerLlave:
            json_response = json_response[primerLlave:ultimaLlave + 1]

    
    
    # Convertir la cadena JSON a un diccionario
    try:
        data = json.loads(json_response)
        return data
    except json.JSONDecodeError as e:
        print("Error al decodificar JSON:", e)
        return None