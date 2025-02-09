
# 🚀 Web Scraper + Bot Telegram  

Este proyecto es un **web scraper** que extrae información de dos sitios web—uno utilizando `requests` y otro con `Selenium`—para gestionar los datos obtenidos, crear un JSON y notificar vía **Telegram** si hay registros nuevos o si cambia la información de alguno ya almacenado.  

✅ **Imagen disponible en DockerHub**: [pinchapapas/webscraper](https://hub.docker.com/r/pinchapapas/webscraper)  

## ⚡ Instalación rápida  

No necesitas modificar el código ni crear una imagen personalizada. Solo descarga `docker-compose.yml`, configura las variables de entorno y ejecútalo:  

```bash
cd /rutaDeDocker-Compose
docker-compose up -d
```

---

## ✨ Características  

✔ **Extracción de datos** de un sitio web de coches.  
✔ **Notificaciones en tiempo real** a través de **Telegram**.  
✔ **Integración con WhatsApp** utilizando la API de **Twilio** (opcional).  
✔ **Ejecución periódica automática**, con un **bucle infinito** y `time.sleep(10 min)`.  
✔ **Fácil configuración** mediante variables de entorno.  

---

## 🛠 Requisitos  

Antes de ejecutar este proyecto, asegúrate de tener instalado:  

- 🐳 **Docker** → Para ejecutar el contenedor.  
- 📦 **Docker Compose** → Para gestionar las variables de entorno.

---

## 🔧 Configuración  

### 1. Clona este repositorio

Si no tienes el repositorio en tu máquina, clónalo usando el siguiente comando:

```bash
git clone https://github.com/alexmartinezmoron/webscraper.git
cd webscraper
```

### 2. Crea tu bot en Telegram  

Para generar el **TELEGRAM_BOT_TOKEN**, sigue estos pasos para crear un bot en Telegram:  

1. Abre Telegram y busca el usuario **@BotFather**.  
2. Inicia una conversación con él y usa el comando `/newbot`.  
3. Sigue las instrucciones y elige un nombre y un nombre de usuario para tu bot (el nombre de usuario debe terminar en **bot**, por ejemplo, `MiScraperBot`).  
4. Una vez creado, **BotFather** te dará un **Token de acceso**. Copia este token y agrégalo en el archivo `.env` en la variable **TELEGRAM_BOT_TOKEN**.  
5. Para obtener el **TELEGRAM_CHAT_ID**, puedes usar el bot **@userinfobot** en Telegram o la API de Telegram para obtener el ID del chat donde se enviarán los mensajes.

### 3. Configura las variables de entorno  

Solo necesitas configurar las variables de entorno. Puedes hacerlo de dos maneras:

#### Opción 1: Edita el archivo `.env`

Crea un archivo `.env` en la raíz del proyecto con los siguientes valores (reemplaza con tus credenciales de Twilio y la URL de tu sitio web):

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

#### Opción 2: Edita directamente el archivo `docker-compose.yml`

Si prefieres, también puedes colocar las variables directamente en el archivo `docker-compose.yml`.  

---

## Docker Hub

El contenedor está disponible en **Docker Hub**. Si prefieres usar el contenedor preconstruido en lugar de crear el tuyo propio, puedes descargar la última versión de la imagen con el siguiente comando:

```bash
docker pull pinchapapas/webscraper:latest
```

Una vez descargado, solo tienes que ejecutar el `docker-compose.yml` como se explicó anteriormente.

---

## 📜 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
