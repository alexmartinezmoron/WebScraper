import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

# URL de la página a scrapear
BASE_URL_FACILITEA = os.getenv("BASE_URL_FACILITEA")

# Configuración de Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecución sin interfaz gráfica
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--ignore-certificate-errors")  # Ignorar errores de SSL
chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")


def get_vehicle_links_facilitea():
    """Obtiene los enlaces de vehículos de la página de Facilitea usando Selenium y los guarda en una lista."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(BASE_URL_FACILITEA)
    
    # Esperar explícitamente a que los enlaces estén disponibles
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.relative h3.leading-5 a")))

    vehicle_data = []  # Lista para guardar la información de los vehículos

    try:
        # Encuentra los elementos que contienen la información del vehículo
        vehicle_elements = driver.find_elements(By.CSS_SELECTOR, "div.relative h3.leading-5 a")

        # Iterar sobre los elementos de vehículo y extraer los datos
        for title_element in vehicle_elements:
            url = title_element.get_attribute("href").strip()  # Obtener la URL del enlace
            # Extraer el título: parte de la URL entre "/ficha/" y el ID (antes del último guion)
            raw_title = url.split("/ficha/")[1].rsplit("-", 2)[0]
            # Formatear el título: reemplazar guiones por espacios y capitalizar adecuadamente
            title = raw_title.replace("-", " ").title()
            product_id = url.split("-")[-1]  # Extrae el ID del producto (última parte de la URL)
            
            # Añadir el vehículo a la lista con precio 0 por defecto
            vehicle_data.append({
                'title': title,
                'id': product_id,
                'url': url,
                'price': "0"  # Precio inicial como string
            })

    except Exception as e:
        print(f"⚠️ Error obteniendo enlaces: {e}")

    finally:
        driver.quit()  # Cierra el navegador

    return update_prices(vehicle_data)


def update_prices(vehicle_data):
    """Accede a cada URL, extrae el precio y actualiza la lista, guardando solo el PVP como string."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    for vehicle in vehicle_data:
        url = vehicle['url']
        try:
            driver.get(url)
            
            # Esperar explícitamente a que el precio esté disponible
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'PVP:')]")))

            # Buscar el texto "PVP:" y extraer el precio que viene después
            pvp_text_element = driver.find_element(By.XPATH, "//p[contains(text(),'PVP:')]")
            price_text = pvp_text_element.text.split("PVP:")[1].strip()  # Tomamos todo el texto después de PVP:
            
            # Solo extraer el PVP antes de cualquier otra parte de texto
            pvp_value = price_text.split(" /")[0].strip()  # Solo tomar el valor antes de " / Precio total a plazos"
            
            # Actualizar el precio en la lista (lo mantenemos como string)
            vehicle['price'] = pvp_value

            print(f"Updated {vehicle['title']} with price: {vehicle['price']}")

        except Exception as e:
            print(f"⚠️ Error actualizando el precio de {vehicle['title']}: {e}")
            vehicle['price'] = "0"  # En caso de error, dejamos el precio como 0 (string)

    driver.quit()  # Cierra el navegador

    return vehicle_data  # Regresamos la lista de vehículos con los precios actualizados


# Ejecutar el proceso
if __name__ == "__main__":
    # Primero obtenemos los datos de los vehículos
    vehicle_data = get_vehicle_links_facilitea()
    
    # Luego actualizamos los precios accediendo a cada URL
    updated_vehicle_data = update_prices(vehicle_data)

    # Imprimir la lista de vehículos con sus precios actualizados
    for vehicle in updated_vehicle_data:
        print(f"Title: {vehicle['title']}, ID: {vehicle['id']}, URL: {vehicle['url']}, Price: {vehicle['price']}")
