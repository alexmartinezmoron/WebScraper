import os
import requests
from bs4 import BeautifulSoup
import re
from twilio.rest import Client  # Librería para Twilio

# Obtener las credenciales y variables desde las variables de entorno
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
MY_WHATSAPP_NUMBER = os.getenv("MY_WHATSAPP_NUMBER")
URL = os.getenv("URL")  # URL de la página a monitorear

# Función para obtener el HTML de la página
def obtener_html(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error {response.status_code}")
        return None

# Función para extraer el número del <h1>
# En mi caso obtengo el número de coches de un h1
def obtener_numero_h1(html):
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1", class_="tablet:text-[28px] laptop:text-4xl font-medium max-tablet:text-3xl max-w-[700px]")
    if h1:
        texto = h1.get_text(strip=True)
        numero = re.search(r"\d+", texto)  # Buscar solo el número dentro del texto
        return numero.group() if numero else None
    return None

# Función para enviar mensaje por WhatsApp usando Twilio
def enviar_whatsapp(mensaje):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=mensaje,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=MY_WHATSAPP_NUMBER
    )
    print(f"✅ Notificación enviada por WhatsApp: {mensaje}")

# Asegurarse de que no existe un directorio con el mismo nombre
if os.path.isdir("numero_anterior.txt"):
    print("Error: 'numero_anterior.txt' es un directorio, no un archivo.")
    exit(1)

# Crear o cargar el último número almacenado (si existe)
try:
    with open("numero_anterior.txt", "r") as f:
        numero_anterior = f.read().strip()
except FileNotFoundError:
    numero_anterior = ""
    with open("numero_anterior.txt", "w") as f:
        f.write("")  # Guardamos un archivo vacío si no existe

# Obtener el HTML actual
html_actual = obtener_html(URL)

if html_actual:
    numero_actual = obtener_numero_h1(html_actual)

    if numero_actual:
        if numero_actual != numero_anterior:
            mensaje = f"⚠️ El número de coches ha cambiado: {numero_actual}"
            print(f"⚠️ {mensaje}")

            # Enviar notificación por WhatsApp
            enviar_whatsapp(mensaje)

            # Actualizar el número almacenado en el archivo
            with open("numero_anterior.txt", "w") as f:
                f.write(numero_actual)
