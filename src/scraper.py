from bs4 import BeautifulSoup
import requests
import re
from quote import Quote
from logger import logger
from loader import Loader
from constants import URL_BASE, URL_PAGE, HEADERS, SEPARATOR, BOOK, WRITING_HAND, RED, RESET

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
        self.header_shown = False  # Controla si el encabezado H1 ya ha sido mostrado
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
                self.soups.append(soup)  # Almacena el objeto BeautifulSoup en la lista
                # Solo muestra el encabezado H1 de la primera página
                if not self.header_shown:
                    self.show_header(soup)
                    self.header_shown = True
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

            self.loader.start()  # Inicia el loader
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
                        
                        author_born_date = about_content.get("author_born_date")
                        author_born_location = about_content.get("author_born_location")
                        author_description = about_content.get("author_description")                   
                    except AttributeError as e:
                        logger.error(f"Error al procesar 'about': {e}")
                    
                    quotes_list.append(Quote(text, author, author_born_date, tag_list, author_born_location, author_description))

        except AttributeError as e:
            logger.error(f"Error al procesar las citas: {e}")
        except Exception as e:
            logger.error(f"Ocurrió un error inesperado: {e}")
        finally:
            self.loader.stop()  # Detiene el loader independientemente del resultado
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
                author_born_date = about_content.find('span', class_='author-born-date').text.strip() if about_content.find('span', class_='author-born-date') else "No birth date found"
                author_born_location = about_content.find('span', class_='author-born-location').text.strip() if about_content.find('span', class_='author-born-location') else "No birth location found"
                author_description = about_content.find('div', class_='author-description').text.strip() if about_content.find('div', class_='author-description') else "No description found"

                return {
                    "author_title": author_title,
                    "author_born_date": author_born_date,
                    "author_born_location": author_born_location,
                    "author_description": author_description
                }
            else:
                return {
                    "author_title": "No title found",
                    "author_born_date": "No birth date found",
                    "author_born_location": "No birth location found",
                    "author_description": "No description found"
                }
        except Exception as e:
            logger.error(f"Error al obtener el contenido de la página 'about': {e}")
            return {
                "author_title": "Error",
                "author_born_date": "Error",
                "author_born_location": "Error",
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
