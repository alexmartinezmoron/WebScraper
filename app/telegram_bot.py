import requests

def send_telegram_message(bot_token, chat_id, message):
    """Envía un mensaje a Telegram y devuelve la respuesta JSON."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, json=payload)

    try:
        return response.json()  # Asegurar que siempre se devuelve un diccionario
    except Exception as e:
        return {"ok": False, "description": f"Error en la respuesta de Telegram: {str(e)}"}

def send_large_message(bot_token, chat_ids, message, chat_id=None):
    """Divide y envía mensajes largos en varias partes a múltiples chat_ids o a un chat_id específico."""
    max_length = 4096
    for i in range(0, len(message), max_length):
        chunk = message[i:i + max_length]
        if chat_id:
            response = send_telegram_message(bot_token, chat_id, chunk)
            if not response or not response.get('ok', False):
                print(f"Error al enviar mensaje a {chat_id}: {response.get('description', 'Desconocido') if response else 'Sin respuesta'}")
            else:
                print(f"Mensaje enviado correctamente a {chat_id}.")
        else:
            for chat_id in chat_ids:  # Enviar a todos los chat_ids
                response = send_telegram_message(bot_token, chat_id, chunk)
                if not response or not response.get('ok', False):
                    print(f"Error al enviar mensaje a {chat_id}: {response.get('description', 'Desconocido') if response else 'Sin respuesta'}")
                else:
                    print(f"Mensaje enviado correctamente a {chat_id}.")
