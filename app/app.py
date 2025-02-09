import os
import json
from webscraperRenew import get_new_vehicles
from telegram_bot import send_large_message
from datetime import datetime
from dotenv import load_dotenv
import time

load_dotenv()

# Variables del bot
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_ids = os.getenv('TELEGRAM_CHAT_IDS')

if chat_ids:
    chat_ids = chat_ids.split(',')  # Lista de chat_ids
else:
    chat_ids = []

# Obtener la fecha y hora actual
def get_today_date():
    return datetime.now().strftime("%d-%m-%Y %H:%M")

def load_processed_vehicles():
    """Carga los vehículos ya procesados desde un archivo JSON."""
    try:
        with open("procesados.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def detect_price_changes(new_vehicles, processed_vehicles):
    """Compara los vehículos nuevos con los procesados y detecta cambios de precio."""
    changed_vehicles = []
    new_vehicles_list = []

    for vehicle in new_vehicles:
        if isinstance(vehicle, dict):  # Aseguramos que el vehicle sea un diccionario
            veh_id = vehicle.get("id")
            title = vehicle.get("title")
            price = vehicle.get("price")
            url = vehicle.get("url")

            if veh_id is None:  # Verifica si falta el ID
                continue

            if vehicle.get("status") == "Nuevo":
                new_vehicles_list.append({
                    "id": veh_id,
                    "title": title,
                    "price": price,
                    "url": url,
                    "status": "Nuevo"
                })
            elif vehicle.get("status") == "Cambio de precio":
                old_price = vehicle.get("old_price")
                changed_vehicles.append({
                    "id": veh_id,
                    "title": title,
                    "price": price,
                    "old_price": old_price,
                    "url": url,
                    "status": "Cambio de precio"
                })
    
    return new_vehicles_list, changed_vehicles

def save_processed_vehicles(processed_vehicles):
    """Guarda la lista actualizada de vehículos en un archivo JSON."""
    with open("procesados.json", "w", encoding="utf-8") as file:
        json.dump(processed_vehicles, file, ensure_ascii=False, indent=4)

def main():
    if not bot_token or not chat_ids:
        print("Error: Token del bot o chat_ids no configurados.")
        return

    while True:  # Bucle infinito para ejecutar cada 10 minutos
        # Cargar datos
        processed_vehicles = load_processed_vehicles()
        new_vehicles = get_new_vehicles()

        # Detectar cambios y nuevos vehículos
        new_vehicles_list, changed_vehicles = detect_price_changes(new_vehicles, processed_vehicles)

        # Si hay vehículos nuevos o cambios de precio, enviarlos por Telegram
        if new_vehicles_list or changed_vehicles:
            today = get_today_date()
            message_text = f"\U0001F514 Novedades: {today} \U0001F514\n"
            send_large_message(bot_token, chat_ids, message_text)
        else:
            print("No hay novedades")

        if new_vehicles_list:
            messages = []

            for vehicle in new_vehicles_list:
                veh_id = vehicle.get("id")
                title = vehicle.get("title")
                price = vehicle.get("price")
                url = vehicle.get("url")

                messages.append(f"\U0001F195 *{title}*\n\U0001F4B0 Precio: {price}\n\U0001F517 [Ver vehículo]({url})\n")

                # Actualizar en el diccionario de procesados
                processed_vehicles[veh_id] = {"title": title, "price": price, "url": url}

            # Enviar mensaje con los vehículos nuevos
            message_text = f"\U0001F514 *Nuevos vehículos encontrados*\n\n" + "\n".join(messages)
            send_large_message(bot_token, chat_ids, message_text)

        # Si hay vehículos con cambio de precio, enviarlos por Telegram
        if changed_vehicles:
            messages = []

            for vehicle in changed_vehicles:
                veh_id = vehicle.get("id")
                title = vehicle.get("title")
                price = vehicle.get("price")
                old_price = vehicle.get("old_price")
                url = vehicle.get("url")

                messages.append(f"\U0001F504 *{title}*\n\U0001F4B0 *Nuevo Precio:* {price} (Antes: {old_price})\n\U0001F517 [Ver vehículo]({url})\n")

                # Actualizar en el diccionario de procesados
                processed_vehicles[veh_id] = {"title": title, "price": price, "url": url}

            # Enviar mensaje con los vehículos que han cambiado de precio
            message_text = f"\U0001F514 *Vehículos con cambio de precio*\n\n" + "\n".join(messages)
            send_large_message(bot_token, chat_ids, message_text)

        # Guardar la nueva lista de procesados
        save_processed_vehicles(processed_vehicles)

        # Esperar 10 minutos antes de la siguiente ejecución
        print("Esperando 10 minutos antes de la siguiente ejecución...")
        time.sleep(600)

if __name__ == "__main__":
    main()