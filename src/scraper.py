from bs4 import BeautifulSoup
import requests
import re
from quote import Quote
from logger import logger
from loader import Loader
from constants import URL_BASE, HEADERS, SEPARATOR, BOOK, WRITING_HAND, RED, RESET

class Scraper:
    """
    Clase para realizar el scraping de una página web y extraer citas y encabezados.

    Atributos:
        soup (BeautifulSoup): Objeto BeautifulSoup que contiene el HTML de la página web.

    Métodos:
        fetch_html(): Obtiene el HTML de la página web y lo almacena en el atributo `soup`.
        get_header(): Extrae y muestra el primer encabezado H1 de la página web.
        get_quotes(): Extrae y devuelve una lista de objetos `Quote` que contienen citas, autores y etiquetas.
        display_quotes(quotes_list): Muestra en pantalla las citas contenidas en la lista `quotes_list`.
    """
    
    def __init__(self):
        """
        Inicializa una nueva instancia de la clase Scraper.\n        
        Configura el atributo `soup` a None.
        """
        self.soup = None
        self.loader = Loader()  # Instancia del loader para mostrar progreso

    def fetch_html(self):
        """
        Obtiene el HTML de la página web especificada en `URL_BASE` y lo analiza usando BeautifulSoup.\n        
        Si ocurre un error al obtener la página o al analizar el HTML, se imprime un mensaje de error.
        """
        try:
            response = requests.get(URL_BASE, headers=HEADERS)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener la página: {e}")
        except Exception as e:
            logger.error(f"Ocurrió un error inesperado: {e}")

    def get_header(self):
        """
        Extrae el primer encabezado H1 de la página web y lo muestra en pantalla.\n
        Si no se encuentra un H1, se indica que no se encontró ninguno. El texto se limpia y se muestra en mayúsculas,
        junto con separadores y etiquetas predefinidas.\n        
        Se maneja el caso en el que no se pueda encontrar el H1 con un mensaje de error.
        """
        try:
            primer_h1 = self.soup.find('h1')
            primer_h1_text = primer_h1.text if primer_h1 else 'No H1 found'
            primer_h1_limpio = re.sub(r'[^a-zA-Z\s]', '', primer_h1_text)  # Limpiar el texto
            print(SEPARATOR)
            print(f"                              {BOOK}  {primer_h1_limpio.strip().upper()}  {WRITING_HAND}")  # Imprimir en mayúsculas
            print(SEPARATOR)
        except AttributeError as e:
            logger.error(f"Error al obtener el encabezado: {e}")
        except Exception as e:
            logger.error(f"Ocurrió un error inesperado: {e}")


    # def get_quotes(self):
    #     """
    #     Extrae citas de la página web y las devuelve como una lista de objetos `Quote`.\n
    #     Cada cita se extrae de un div con la clase 'quote', incluyendo el texto de la cita, el autor y las etiquetas.\n        
    #     Si ocurre un error al procesar las citas, se imprime un mensaje de error y se devuelve una lista vacía.\n        
    #     Returns:
    #         List[Quote]: Lista de objetos `Quote` con las citas extraídas.
    #     """
    #     quotes_list = []
    #     try:
    #         quotes = self.soup.find_all('div', class_='quote')
    #         for quote in quotes:
    #             text = quote.find('span', class_='text').text.strip()
    #             author = quote.find('small', class_='author').text.strip()
    #             tags = quote.find_all('a', class_='tag')
    #             tag_list = [tag.text.strip().capitalize() for tag in tags]
    #             about = quote.find('a', text='(about)')
    #             try:
    #                 about_url = about.get('href')
    #                 about_content = self.fetch_about_content(about_url)
                    
    #                 # Acceder a los elementos del diccionario about_content
    #                 author_born_date = about_content.get("author_born_date")
    #                 author_born_location = about_content.get("author_born_location")
    #                 author_description = about_content.get("author_description")                   
    #             except AttributeError as e:
    #                 logger.error(f"Error al procesar 'about': {e}")
                
    #             quotes_list.append(Quote(text, author, author_born_date, tag_list, author_born_location, author_description))

    #     except AttributeError as e:
    #         logger.error(f"Error al procesar las citas: {e}")
    #     except Exception as e:
    #         logger.error(f"Ocurrió un error inesperado: {e}")
    #     return quotes_list

    def get_quotes(self):
        """
        Extrae citas de la página web y las devuelve como una lista de objetos `Quote`.
        Returns:
            List[Quote]: Lista de objetos `Quote` con las citas extraídas.
        """
        self.loader.start()  # Inicia el loader

        quotes_list = []
        try:
            quotes = self.soup.find_all('div', class_='quote')
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
