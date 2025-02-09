import os
from twilio.rest import Client  # Librería para Twilio

# Obtener las credenciales y variables desde las variables de entorno
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
MY_WHATSAPP_NUMBER = os.getenv("MY_WHATSAPP_NUMBER")

# Función para enviar mensaje por WhatsApp usando Twilio
def enviar_whatsapp(mensaje):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=mensaje,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=MY_WHATSAPP_NUMBER
    )
    print(f"✅ Notificación enviada por WhatsApp: {mensaje}")