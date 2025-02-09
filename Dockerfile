# Usamos una imagen base de Python ligera
FROM python:3.9-slim

# Instalamos las dependencias necesarias
RUN apt-get update && apt-get install -y \
    python3-pip \
    wget \
    unzip \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Instalamos Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Instalamos ChromeDriver
RUN CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos los archivos antes de instalar dependencias para aprovechar mejor la caché de Docker
COPY requirements.txt .

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos la aplicación después de instalar las dependencias
COPY app/ .

# Asignamos permisos totales a la carpeta /app
RUN chmod -R 777 /app

# Establecemos la variable de entorno para Python (mejor para logs)
ENV PYTHONUNBUFFERED=1

# Comando por defecto para ejecutar el script
CMD ["python", "app.py"]