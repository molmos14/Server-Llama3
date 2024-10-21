# README.md

## Proyecto: Chatbot de Zazil

Este proyecto implementa un **chatbot especializado en temas de menstruación**, desarrollado para brindar información clara y útil sobre el ciclo menstrual, productos relacionados, y más. Utiliza **Flask** para crear una API que gestiona las solicitudes, y **Ollama** como motor de IA con el modelo **LLaMA 3.1** para generar respuestas.

---

## Contenido del Repositorio

- **Dockerfile**: Configura el entorno de Docker para ejecutar el servidor Flask junto con Ollama.
- **response_cache.json**: Archivo JSON que actúa como caché de respuestas del chatbot.
- **server.py**: Código principal que define la API Flask y maneja las consultas con Ollama.

---

## Requisitos

- Docker instalado: [Guía de instalación](https://docs.docker.com/get-docker/)
- Conexión a internet para descargar el modelo **LLaMA 3.1** desde Ollama.

---

## Instrucciones de Uso

### 1. Construir y ejecutar el contenedor Docker

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone <URL-del-repositorio>
   cd <directorio-del-repositorio>
   ```

2. Construye la imagen de Docker:
   ```bash
   docker build -t chatbot-zazil .
   ```

3. Ejecuta el contenedor:
   ```bash
   docker run -p 5000:5000 chatbot-zazil
   ```

Esto expondrá el servicio Flask en el puerto **5000**.

### 2. Probar la API

- **Endpoint**: `/chat`
- **Método**: `POST`
- **Formato del cuerpo de la solicitud**:
  ```json
  {
    "messages": [
      { "role": "user", "content": "Hola" }
    ]
  }
  ```

- **Ejemplo de comando curl**:
  ```bash
  curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hola"}]}'
  ```

---

## Descripción de los Archivos

### Dockerfile
Este archivo define la configuración del entorno del contenedor Docker. Realiza las siguientes acciones:

- Usa una imagen base de **Ubuntu 20.04**.
- Instala **Python 3** y **Flask**.
- Descarga e inicia el servicio **Ollama** y el modelo **LLaMA 3.1**.
- Copia los archivos necesarios para la aplicación, incluyendo el **caché de respuestas**.

### response_cache.json
Un archivo JSON que almacena respuestas predefinidas para las preguntas más frecuentes. Esto permite evitar consultas repetidas al modelo LLaMA 3.1, mejorando la eficiencia.

### server.py
El archivo principal del proyecto que:

1. Define la API Flask para procesar consultas.
2. Normaliza mensajes de usuario para asegurar respuestas consistentes.
3. Consulta el caché o utiliza el modelo LLaMA 3.1 para generar nuevas respuestas.
4. Bloquea solicitudes simultáneas usando un **lock** para evitar conflictos.

---

## Flujo de Trabajo del Chatbot

1. **El usuario envía un mensaje** a través de la API.
2. **El servidor Flask** normaliza el mensaje y busca una respuesta en el caché.
3. Si no hay una respuesta en caché, **el modelo LLaMA 3.1** genera una nueva.
4. La respuesta se envía al usuario y, si es nueva, se guarda en el caché para futuras consultas.

---

## Personalización

- **Agregar respuestas predefinidas**: Puedes editar `response_cache.json` para incluir más preguntas y respuestas comunes.
- **Modificar el comportamiento del chatbot**: Ajusta las reglas en el mensaje del sistema dentro del archivo `server.py`.

---

## Notas Adicionales

- **Escalabilidad**: El servicio usa un bloqueo (`Lock`) para evitar que múltiples solicitudes se procesen al mismo tiempo. Esto garantiza estabilidad, especialmente en entornos con alta concurrencia.
- **Conexión con humanos**: Si el usuario solicita hablar con una persona, el chatbot sugiere contactar al equipo de Zazil por teléfono o redes sociales.

---

## Contribuciones

Si deseas contribuir a este proyecto, por favor:

1. Realiza un fork del repositorio.
2. Crea una rama para tu feature o fix:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Envía tus cambios mediante un Pull Request.

---

## Contacto

Si tienes preguntas o comentarios, no dudes en contactarnos a través de nuestras redes sociales en **@molmos16** o por teléfono: **+52 4141403437**.
