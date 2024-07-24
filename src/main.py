"""
Este script es el punto de entrada principal para ejecutar el proceso de scraping web.

Importa la clase Scraper desde el módulo scraper, crea una instancia de esta clase,
y luego ejecuta los métodos para obtener el HTML de la página, extraer y mostrar el encabezado H1,
y extraer y mostrar citas de la página web.

Usage:
    Ejecuta este script directamente desde la línea de comandos.
"""

from scraper import Scraper

def main():
    """
    Función principal que crea una instancia de Scraper y ejecuta el flujo principal de scraping.

    1. Crea una instancia de la clase Scraper.
    2. Obtiene el HTML de la página web.
    3. Extrae y muestra el primer encabezado H1.
    4. Extrae las citas de la página web.
    5. Muestra las citas en la salida estándar.
    """
    # Crear una instancia de la clase Scraper
    scpr = Scraper()
    
    # Obtener el HTML de la página web y almacenarlo en el atributo 'soup'
    scpr.fetch_html()
    
    # Extraer y mostrar el primer encabezado H1 de la página web
    scpr.get_header()
    
    # Extraer una lista de citas desde la página web
    quotes = scpr.get_quotes()
    
    # Mostrar las citas contenidas en la lista 'quotes'
    scpr.display_quotes(quotes)

# Ejecutar la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main()
