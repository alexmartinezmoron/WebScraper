import requests
from bs4 import BeautifulSoup
import json
import os
import time
from webscraperFacilitea import get_vehicle_links_facilitea

# 🔗 URL base para scraping
BASE_URL_RENEW = os.getenv("BASE_URL_RENEW")
BASE_URL_RENEW_PAGINADO = os.getenv("BASE_URL_RENEW_PAGINADO")

# 📁 Archivo donde guardamos los vehículos procesados
PROCESSED_FILE = "procesados.json"

# 📥 Máximo de intentos al hacer una solicitud web
MAX_RETRIES = 3
RETRY_DELAY = 2  # segundos

def get_vehicle_links_renew(page_number):
    """Obtiene los enlaces de vehículos de la página de Renault Renew."""
    url = f"{BASE_URL_RENEW_PAGINADO}{page_number}"
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=10)  # ⏳ 10s de timeout
            if response.status_code == 200:
                break
            print(f"⚠️ Error {response.status_code} en página {page_number}, intento {attempt+1}")
            time.sleep(RETRY_DELAY)
        except requests.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            time.sleep(RETRY_DELAY)
    else:
        return []  # ❌ No se pudo obtener la página después de varios intentos

    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    for a_tag in soup.find_all("a", {"class": "UCIVehicleCard__link"}):
        title = a_tag.get("title", "").strip()
        if "Esprit" in title:
            href = a_tag.get("href", "").strip()
            price_span = a_tag.find_next("span", class_="UCIVehicleCard__taxLabel")
            price = price_span.text.strip() if price_span else "No disponible"
            product_id = href.split("=")[-1]  # Extraemos el productId del enlace

            links.append({
                "id": product_id,
                "title": title,
                "url": f"{BASE_URL_RENEW}{href}",
                "price": price
            })

    return links

def load_processed_products():
    """Carga los vehículos procesados desde un archivo JSON."""
    if os.path.exists(PROCESSED_FILE):
        try:
            with open(PROCESSED_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            print("⚠️ Error al leer procesados.json, creando uno nuevo.")
    return {}  # Devuelve un diccionario vacío si hay error

def save_processed_products(processed_data):
    """Guarda los vehículos procesados en un archivo JSON."""
    with open(PROCESSED_FILE, "w", encoding="utf-8") as file:
        json.dump(processed_data, file, ensure_ascii=False, indent=4)

def get_new_vehicles():
    """Obtiene nuevos vehículos y detecta cambios de precio."""
    processed_products = load_processed_products()
    new_or_changed_vehicles = []
    updated_products = processed_products.copy()

    # Scraping de Renault Renew
    for page_number in range(1, 26):
        print(f"📄 Scrapeando página {page_number} de Renault Renew...")
        page_links = get_vehicle_links_renew(page_number)

        for vehicle in page_links:
            veh_id = vehicle["id"]
            title = vehicle["title"]
            price = vehicle["price"]
            url = vehicle["url"]

            # 🚗 Nuevo vehículo encontrado
            if veh_id not in processed_products:
                new_or_changed_vehicles.append({
                    "id": veh_id,
                    "title": title,
                    "price": price,
                    "url": url,
                    "status": "Nuevo"
                })
            else:
                old_price = processed_products.get(veh_id, {}).get("price", None)
                if old_price and old_price != price:
                    # 🔄 Cambio de precio detectado
                    new_or_changed_vehicles.append({
                        "id": veh_id,
                        "title": title,
                        "price": price,
                        "old_price": old_price,
                        "url": url,
                        "status": "Cambio de precio"
                    })

            # 📝 Guardar la versión más reciente del vehículo
            updated_products[veh_id] = {"title": title, "price": price, "url": url}

    # Scraping de Facilitea
    print(f"📄 Scrapeando la página de Facilitea...")
    page_links = get_vehicle_links_facilitea()

    for vehicle in page_links:
        veh_id = vehicle["id"]
        title = vehicle["title"]
        price = vehicle["price"]
        url = vehicle["url"]

        # 🚗 Nuevo vehículo encontrado
        if veh_id not in processed_products:
            new_or_changed_vehicles.append({
                "id": veh_id,
                "title": title,
                "price": price,
                "url": url,
                "status": "Nuevo"
            })
        else:
            old_price = processed_products.get(veh_id, {}).get("price", None)
            if old_price and old_price != price:
                # 🔄 Cambio de precio detectado
                new_or_changed_vehicles.append({
                    "id": veh_id,
                    "title": title,
                    "price": price,
                    "old_price": old_price,
                    "url": url,
                    "status": "Cambio de precio"
                })

        # 📝 Guardar la versión más reciente del vehículo
        updated_products[veh_id] = {"title": title, "price": price, "url": url}

    # 💾 Guardar los productos actualizados en el JSON
    save_processed_products(updated_products)

    return new_or_changed_vehicles

# Ejecutar la función para obtener nuevos vehículos
if __name__ == "__main__":
    nuevos_vehiculos = get_new_vehicles()
    print(f"Nuevos o cambiados vehículos: {nuevos_vehiculos}")