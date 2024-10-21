from flask import Flask, request, Response
import ollama
from threading import Lock
import json
import os
import unicodedata
import re

app = Flask(__name__)
lock = Lock()  # Para evitar procesar múltiples solicitudes a la vez

# Load the response cache
cache_file_path = 'response_cache.json'
if os.path.exists(cache_file_path):
    with open(cache_file_path, 'r', encoding='utf-8') as f:
        response_cache = json.load(f)
else:
    response_cache = {}

# Define el mensaje del sistema para las respuestas predeterminadas
system_message = {
    "role": "system",
    "content": """
    Eres un asistente virtual especializado en menstruación, creado por la empresa Zazil. Tu función principal es proporcionar información precisa y útil sobre la menstruación y temas relacionados. Sigue estas reglas estrictamente:

    1. **Saludo personalizado**:
        - Si el usuario dice "Hola, soy [nombre]", responde amablemente con:
          "¡Hola, [nombre]! Es un placer conocerte. Bienvenido al chatbot de Zazil. ¿En qué puedo ayudarte hoy?"
        - Si el usuario solo dice "Hola", salúdalo cordialmente y ofrece tu ayuda:
          "¡Hola! Bienvenido al chatbot de Zazil. ¿Cómo puedo asistirte con respecto a la menstruación?"

    2. **Respuestas a temas fuera de la menstruación**:
        - Si el usuario pregunta sobre temas no relacionados con la menstruación, responde de manera educada:
          "Lo siento, solo puedo responder preguntas relacionadas con la menstruación y temas asociados."

    3. **Usuarios masculinos y temas relacionados**:
        - Si el usuario es hombre, pero hace preguntas sobre la menstruación o temas asociados, responde de forma precisa y útil. No discrimines por género.
        - Si el usuario pregunta sobre productos relacionados con la menstruación, como condones, pastillas anticonceptivas o la copa menstrual, proporciona respuestas claras y concisas.

    4. **Preguntas sobre la menstruación**:
        - Si el usuario realiza una pregunta directamente relacionada con la menstruación, respóndela de manera inmediata y detallada.

    5. **Solicitudes para hablar con un humano**:
        - Si el usuario solicita hablar con una persona, responde:
          "¡Claro! Puedes contactarnos al 55 1234 5678 o a través de nuestras redes sociales en @zazil. Estoy aquí si necesitas más información."

    Mantén siempre un tono amigable y profesional, proporcionando información confiable y relevante.
    """
}

def normalize_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove accents and special characters
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Replace spaces with underscores
    text = text.replace(' ', '_')
    return text

@app.route('/chat', methods=['POST'])
def chat():
    with lock:  # Bloquea el procesamiento de múltiples solicitudes simultáneas
        data = request.json
        user_messages = data.get('messages', [])
        
        # Asegúrate de que haya mensajes de usuario antes de procesar
        if not user_messages:
            return Response("No se recibieron mensajes.", status=400)

        user_message = user_messages[-1]['content']  # Get the last user message
        normalized_message = normalize_text(user_message)  # Normalize the user message

        # Check if the response is already in the cache
        if normalized_message in response_cache:
            full_response = response_cache[normalized_message]
        else:
            messages = [system_message] + user_messages
            
            # Generar la respuesta utilizando el modelo
            response = ollama.chat(model='llama3.1', messages=messages, stream=False)
            full_response = response['message']['content']
            
            # Update the cache
            response_cache[normalized_message] = full_response
            with open(cache_file_path, 'w', encoding='utf-8') as f:
                json.dump(response_cache, f, ensure_ascii=False, indent=4)

        # Añade un log para verificar la respuesta
        print(f"Response generated: {full_response}")  # Asegúrate de que solo se genere una respuesta

        headers = {'Content-Type': 'text/plain; charset=utf-8'}
        return Response(full_response, headers=headers)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
