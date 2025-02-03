
# Web Scraper + Twilio WhatsApp

Este proyecto es un **web scraper** que extrae información de un sitio web y la envía a través de WhatsApp utilizando la API de **Twilio**. El contenedor Docker ya está preparado para que solo tengas que lanzar el archivo `docker-compose.yml` con tus variables de entorno personalizadas.

No necesitas editar el código ni crear una imagen personalizada, solo configura las variables de entorno y ejecuta el contenedor.

## Características
- **Extracción de datos** de un sitio web de coches.
- **Envío de notificaciones** a través de WhatsApp utilizando la API de Twilio.
- **Ejecutado periódicamente** con cron en Docker.
- Configuración fácil mediante variables de entorno.

## Requisitos

Antes de ejecutar este proyecto, necesitarás tener las siguientes herramientas instaladas:

- **Docker**: Para crear y ejecutar contenedores.
- **Docker Compose**: Para gestionar el contenedor y las variables de entorno.

## Configuración

1. **Clona este repositorio**:

   Si no tienes el repositorio en tu máquina, clónalo usando el siguiente comando:

   ```bash
   git clone https://github.com/alexmartinezmoron/webscraper.git
   cd webscraper
   ```

2. **Configura las variables de entorno**:

   Solo necesitas configurar las variables de entorno. Puedes hacerlo de dos maneras:

   - **Opción 1: Edita el archivo `.env`**. Crea un archivo `.env` en la raíz del proyecto con los siguientes valores (reemplaza con tus credenciales de Twilio y la URL de tu sitio web):

     ```env
     TWILIO_SID=tu_sid
     TWILIO_AUTH_TOKEN=tu_token
     TWILIO_WHATSAPP_NUMBER=whatsapp:+123456789
     MY_WHATSAPP_NUMBER=whatsapp:+123456789
     URL="https://faciliteacoches.com/coches?search=golf"
     ```

   - **Opción 2: Edita directamente el archivo `docker-compose.yml`**. Si prefieres, también puedes colocar las variables directamente en el archivo `docker-compose.yml`.

3. **Configura Docker Compose**:

   El proyecto ya incluye un archivo `docker-compose.yml` configurado. Asegúrate de que el archivo `.env` esté presente en la misma carpeta que el archivo `docker-compose.yml`. Este archivo configurará el contenedor, las variables de entorno y cómo ejecutar el scraper.

4. **Construye y ejecuta el contenedor**:

   Para construir y ejecutar el contenedor con las variables de entorno definidas, solo ejecuta el siguiente comando:

   ```bash
   docker-compose up --build
   ```

   Esto descargará la imagen, instalará las dependencias necesarias y ejecutará el scraper de forma periódica.

## Cron Jobs

El scraper está configurado para ejecutarse cada hora utilizando **cron**. Los resultados del scraper se guardarán en el archivo `/var/log/cron.log`, donde podrás revisar los logs de ejecución.

## Variables de Entorno

Las siguientes variables de entorno se usan para configurar el comportamiento del scraper:

- `TWILIO_SID`: Tu **SID de Twilio**.
- `TWILIO_AUTH_TOKEN`: Tu **token de autenticación de Twilio**.
- `TWILIO_WHATSAPP_NUMBER`: El número de **WhatsApp de Twilio** desde el que se enviarán los mensajes (en formato `whatsapp:+<número>`).
- `MY_WHATSAPP_NUMBER`: Tu número de **WhatsApp** al que se enviarán las notificaciones (en formato `whatsapp:+<número>`).
- `URL`: La **URL del sitio web** de donde el scraper extraerá los datos.

## Docker Hub

El contenedor está disponible en **Docker Hub**. Si prefieres usar el contenedor preconstruido en lugar de crear el tuyo propio, puedes descargar la última versión de la imagen con el siguiente comando:

```bash
docker pull pinchapapas/webscraper:latest
```

Una vez descargado, solo tienes que ejecutar el `docker-compose.yml` como se explicó anteriormente.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
