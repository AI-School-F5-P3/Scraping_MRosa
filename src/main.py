import sys
import os
# Añade el directorio raíz al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from scraper import Scraper
from src.utils.logger import logger

async def main():
    """
    Función principal que crea una instancia de Scraper y ejecuta el flujo principal de scraping.

    1. Crea una instancia de la clase Scraper.
    2. Obtiene el HTML de la página web.
    3. Extrae las citas de la página web.
    4. Muestra las citas en la salida estándar.
    """
    try:
        # Crear una instancia de la clase Scraper
        scpr = Scraper()
        
        # Obtener el HTML de la página web y almacenarlo en el atributo 'soup'
        scpr.fetch_html()
                
        # Extraer una lista de citas desde la página web
        quotes = scpr.get_quotes()
        
        # Mostrar las citas contenidas en la lista 'quotes'
        # scpr.display_quotes(quotes)
        await scpr.save_quotes_to_db(quotes)
        
    
    except Exception as e:
        # Manejar cualquier excepción inesperada que ocurra durante el flujo principal
        logger.error(f"Ocurrió un error durante el flujo principal: {e}")

# Ejecutar la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    asyncio.run(main())
