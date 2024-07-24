from bs4 import BeautifulSoup
import requests
import re
from quote import Quote
from constants import URL_BASE, HEADERS, separator, BOOK, WRITING_HAND

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
            print(f"Error al obtener la página: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

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
            print(separator)
            print(f"                              {BOOK}  {primer_h1_limpio.strip().upper()}  {WRITING_HAND}")  # Imprimir en mayúsculas
            print(separator)
        except AttributeError as e:
            print(f"Error al obtener el encabezado: {e}")

    def get_quotes(self):
        """
        Extrae citas de la página web y las devuelve como una lista de objetos `Quote`.\n
        Cada cita se extrae de un div con la clase 'quote', incluyendo el texto de la cita, el autor y las etiquetas.\n        
        Si ocurre un error al procesar las citas, se imprime un mensaje de error y se devuelve una lista vacía.\n        
        Returns:
            List[Quote]: Lista de objetos `Quote` con las citas extraídas.
        """
        quotes_list = []
        try:
            quotes = self.soup.find_all('div', class_='quote')
            for quote in quotes:
                text = quote.find('span', class_='text').text.strip()
                author = quote.find('small', class_='author').text.strip()
                tags = quote.find_all('a', class_='tag')
                tag_list = [tag.text.strip().capitalize() for tag in tags]
                quotes_list.append(Quote(text, author, tag_list))
        except AttributeError as e:
            print(f"Error al procesar las citas: {e}")
        return quotes_list

    def display_quotes(self, quotes_list):
        """
        Muestra en pantalla las citas contenidas en la lista `quotes_list`.\n
        Cada cita se muestra utilizando el método `display` del objeto `Quote`.\n        
        Args:
            quotes_list (List[Quote]): Lista de objetos `Quote` que se desea mostrar.
        """
        for quote in quotes_list:
            quote.display()
