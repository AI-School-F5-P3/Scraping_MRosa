import sys
import os
# Añade el directorio raíz al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bs4 import BeautifulSoup
import requests
import re
from quote import Quote
from src.utils.logger import logger
from src.utils.loader import Loader
from src.utils.constants import URL_BASE, URL_PAGE, HEADERS, SEPARATOR, BOOK, WRITING_HAND, TWO_OCLOCK, LIGHT_CYAN, RED, PASTEL_YELLOW, PASTEL_PINK, SMILE, CELEBRATION, GREEN, RESET

from database import SessionLocal

class Scraper:
    """
    Clase para realizar el scraping de una página web y extraer citas y encabezados.

    Atributos:
        soups (List[BeautifulSoup]): Lista de objetos BeautifulSoup que contienen el HTML de cada página web.
        header_shown (bool): Controla si el encabezado H1 ya ha sido mostrado.

    Métodos:
        fetch_html(): Obtiene el HTML de las páginas web especificadas en el rango de páginas y almacena cada página en `self.soups`.
        get_header(): Extrae y muestra el primer encabezado H1 de la página web.
        get_quotes(): Extrae y devuelve una lista de objetos `Quote` que contienen citas, autores y etiquetas.
        display_quotes(quotes_list): Muestra en pantalla las citas contenidas en la lista `quotes_list`.
    """
    
    def __init__(self):
        self.soups = []  # Lista para almacenar los objetos BeautifulSoup de todas las páginas
        self.loader = Loader()  # Instancia del loader para mostrar progreso


    def fetch_html(self):
        """
        Obtiene el HTML de las páginas web especificadas en el rango de páginas y almacena cada página en `self.soups`.
        """
        try:
            for i in range(1, 11):  # Ajusta el rango según el número total de páginas
                URL_FINAL = f"{URL_BASE}{URL_PAGE}{i}"
                response = requests.get(URL_FINAL, headers=HEADERS)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                # Solo muestra el encabezado H1 de la primera página
                if i == 1:
                    self.show_header(soup)
                    # self.loader.start()  # Inicia el loader
                    print(f"\n| {LIGHT_CYAN}Scrapeando... {TWO_OCLOCK}{RESET}\n")

                self.soups.append(soup)  # Almacena el objeto BeautifulSoup en la lista

        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener la página: {e}")
        except Exception as e:
            logger.error(f"Ocurrió un error inesperado: {e}")


    def show_header(self, soup):
        """
        Muestra el primer encabezado H1 de una página web.\n
        Si no se encuentra un H1, se indica que no se encontró ninguno. El texto se limpia y se muestra en mayúsculas,
        junto con separadores y etiquetas predefinidas.\n        
        Se maneja el caso en el que no se pueda encontrar el H1 con un mensaje de error.
        
        Args:
            soup (BeautifulSoup): El objeto BeautifulSoup de la página web.
        """
        try:
            primer_h1 = soup.find('h1')
            primer_h1_text = primer_h1.text if primer_h1 else 'No H1 found'
            primer_h1_limpio = re.sub(r'[^a-zA-Z\s]', '', primer_h1_text)  # Limpiar el texto
            print(SEPARATOR)
            print(f"                              {BOOK}  {primer_h1_limpio.strip().upper()}  {WRITING_HAND}")  # Imprimir en mayúsculas
            print(SEPARATOR)

            # self.loader.start()  # Inicia el loader

        except AttributeError as e:
            logger.error(f"Error al obtener el encabezado: {e}")
        except Exception as e:
            logger.error(f"Ocurrió un error inesperado: {e}")

    def get_quotes(self):
        """
        Extrae citas de todas las páginas web almacenadas en `self.soups` y las devuelve como una lista de objetos `Quote`.
        Returns:
            List[Quote]: Lista de objetos `Quote` con las citas extraídas.
        """

        quotes_list = []
        try:
            for soup in self.soups:
                quotes = soup.find_all('div', class_='quote')
                for quote in quotes:
                    text = quote.find('span', class_='text').text.strip()
                    author = quote.find('small', class_='author').text.strip()
                    tags = quote.find_all('a', class_='tag')
                    tag_list = [tag.text.strip().capitalize() for tag in tags]
                    about = quote.find('a', text='(about)')
                    try:
                        about_url = about.get('href')
                        about_content = self.fetch_about_content(about_url)
                        
                        author_birthdate = about_content.get("author_birthdate")
                        author_birthplace = about_content.get("author_birthplace")
                        author_description = about_content.get("author_description")                   
                    except AttributeError as e:
                        logger.error(f"Error al procesar 'about': {e}")
                    
                    quotes_list.append(Quote(text, author, author_birthdate, tag_list, author_birthplace, author_description))

        except AttributeError as e:
            logger.error(f"Error al procesar las citas: {e}")
        except Exception as e:
            logger.error(f"Ocurrió un error inesperado: {e}")
        # finally:
            # self.loader.stop()  # Detiene el loader independientemente del resultado
        return quotes_list
    

    def fetch_about_content(self, about_url):
        """
        Realiza una solicitud HTTP para obtener el contenido de la página "about".
        
        Args:
            about_url (str): La URL de la página "about".
        
        Returns:
            dict: Un diccionario con la información del autor o un mensaje de error.
        """
        try:
            response = requests.get(f"{URL_BASE}{about_url}", headers=HEADERS)
            response.raise_for_status()
            about_soup = BeautifulSoup(response.text, "html.parser")
            about_content = about_soup.find('div', class_='author-details')
            
            if about_content:
                author_title = about_content.find('h3', class_='author-title').text.strip() if about_content.find('h3', class_='author-title') else "No title found"
                author_birthdate = about_content.find('span', class_='author-born-date').text.strip() if about_content.find('span', class_='author-born-date') else "No birth date found"
                author_birthplace = about_content.find('span', class_='author-born-location').text.strip() if about_content.find('span', class_='author-born-location') else "No birth location found"
                author_description = about_content.find('div', class_='author-description').text.strip() if about_content.find('div', class_='author-description') else "No description found"

                return {
                    "author_title": author_title,
                    "author_birthdate": author_birthdate,
                    "author_birthplace": author_birthplace,
                    "author_description": author_description
                }
            else:
                return {
                    "author_title": "No title found",
                    "author_birthdate": "No birth date found",
                    "author_birthplace": "No birth location found",
                    "author_description": "No description found"
                }
        except Exception as e:
            logger.error(f"Error al obtener el contenido de la página 'about': {e}")
            return {
                "author_title": "Error",
                "author_birthdate": "Error",
                "author_birthplace": "Error",
                "author_description": "Error"
            }
        
    def display_quotes(self, quotes_list):
        """
        Muestra en pantalla las citas contenidas en la lista `quotes_list`.\n
        Cada cita se muestra utilizando el método `display` del objeto `Quote`.\n        
        Args:
            quotes_list (List[Quote]): Lista de objetos `Quote` que se desea mostrar.
        """
        for quote in quotes_list:
            quote.display()

    async def save_quotes_to_db(self, quotes_list):
        """Guarda todas las citas en la base de datos."""
        total_quotes = len(quotes_list)
        print(f"{PASTEL_PINK}Total de citas a procesar: {total_quotes}{RESET}")
        
        async with SessionLocal() as session:
            try:
                for index, quote in enumerate(quotes_list, start=1):
                    try:
                        print(f"\n{BOOK} {PASTEL_YELLOW} Cita {index} ·································································································{RESET}\n")
                        await quote.save(session)
                    except Exception as e:
                        print(f"{RED}Error al guardar la cita {index}: {e}{RESET}")
                        raise
                print(f"\n\n{SMILE} {GREEN} Se han insertado {total_quotes} citas correctamente en la base de datos. {CELEBRATION} {RESET}\n\n")
            except Exception as e:
                print(f"{RED}Error al procesar las citas: {e}{RESET}")



                