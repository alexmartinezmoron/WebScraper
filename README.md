
# Web Scraper + Bot Telegram

Este proyecto es un **web scraper** que extrae información de dos sitios web uno utilizando request y otro sellenium despues de gestiona la informacion obtenida creando un json y notifica via Telegram si hay algun registro nuevo o si cambia la informacion de alguno ya almacenado. Hay una imagen subida a DockerHub puedes visitar el repositorio https://hub.docker.com/r/pinchapapas/webscraper.

No necesitas editar el código ni crear una imagen personalizada, solo descarga docker-compose.yml configura las variables de entorno lanzalo.
```bash
cd /rutaDeDocker-Compose
docker-compose up -d
```

## Características
- **Extracción de datos** de un sitio web de coches.
- **Envío de notificaciones** a través de Telegram utilizando un bot.
- **Envío de notificaciones** a través de WhatsApp utilizando la API de Twilio puedes editar el proyecto para enviar notificaciones con Twilio_bot.
- **Ejecutado periódicamente**  bucle infinito con un time.sleep de 10 min.
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

2.Crea tu bot en Telegram:

   Para generar el TELEGRAM_BOT_TOKEN, sigue estos pasos para crear un bot en Telegram:
   
   Abre Telegram y busca el usuario @BotFather.
   Inicia una conversación con él y usa el comando /newbot.
   Sigue las instrucciones y elige un nombre y un nombre de usuario para tu bot (el nombre de usuario debe terminar en bot, por ejemplo, MiScraperBot).
   Una vez creado, BotFather te dará un Token de acceso. Copia este token y agrégalo en el archivo .env en la variable TELEGRAM_BOT_TOKEN.
   Para obtener el TELEGRAM_CHAT_ID, puedes usar el bot @userinfobot en Telegram o la API de Telegram para obtener el ID del chat donde se enviarán los mensajes.  


3. **Configura las variables de entorno**:

   Solo necesitas configurar las variables de entorno. Puedes hacerlo de dos maneras:

   - **Opción 1: Edita el archivo `.env`**. Crea un archivo `.env` en la raíz del proyecto con los siguientes valores (reemplaza con tus credenciales de Twilio y la URL de tu sitio web):

     ```env
      BASE_URL_FACILITEA="https://url-a-scrapear"
      BASE_URL_RENEW="https://url-a-scrapear"
      BASE_URL_RENEW_PAGINADO="https://url-a-scrapear"
      TELEGRAM_BOT_TOKEN=tu_token
      TELEGRAM_CHAT_ID_User1=123456789
      TELEGRAM_CHAT_ID_User2=123456789
      TELEGRAM_CHAT_ID_User3=123456789
      TELEGRAM_CHAT_IDS=123456789,123456789,123456789
      TWILIO_SID=tu_sid
      TWILIO_AUTH_TOKEN=tu_token
      TWILIO_WHATSAPP_NUMBER=whatsapp:+123456789
      MY_WHATSAPP_NUMBER=whatsapp:+123456789
    ```

   - **Opción 2: Edita directamente el archivo `docker-compose.yml`**. Si prefieres, también puedes colocar las variables directamente en el archivo `docker-compose.yml`.

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
