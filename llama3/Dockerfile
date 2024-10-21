# Utilizamos una imagen base de Ubuntu
FROM ubuntu:20.04

# Actualizamos el sistema y instalamos dependencias necesarias
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip

# Instalamos Ollama desde el script proporcionado
RUN curl -fsSL https://ollama.com/install.sh | sh

# Iniciamos Ollama antes de descargar el modelo
RUN ollama serve & sleep 5 && ollama pull llama3.1

# Creamos un directorio de trabajo
WORKDIR /app

# Copiamos los archivos necesarios
COPY server.py /app/
COPY response_cache.json /app/  
# Copiamos el archivo JSON para el cache

# Instalamos las dependencias de Python
RUN pip3 install flask
RUN pip3 install ollama

# Exponemos el puerto 5000 para Flask
EXPOSE 5000

# Iniciamos Ollama antes de ejecutar la app
CMD ollama serve & python3 server.py
