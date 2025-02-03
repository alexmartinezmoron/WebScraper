# Usamos una imagen base de Python
FROM python:3.9-slim

# Instalamos cron y otras dependencias necesarias
RUN apt-get update && apt-get install -y cron

# Establecemos el directorio de trabajo en el contenedor
WORKDIR /app

# Copiamos los archivos del proyecto al contenedor
COPY . /app

# Instalamos las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el archivo crontab con la configuración para ejecutar el script cada hora
COPY crontab /etc/cron.d/webscraper-cron

# Establecemos permisos para el archivo crontab
RUN chmod 0644 /etc/cron.d/webscraper-cron


# Exponemos el puerto (opcional, si lo necesitas)
EXPOSE 8080

# Comando para iniciar cron y ejecutar el script
CMD ["cron", "-f"]
