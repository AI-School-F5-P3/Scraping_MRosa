from bs4 import BeautifulSoup
import requests
import re

# Definición de colores, estilos e iconos
# Colores pastel personalizados


ITALIC = "\033[3m"
RESET = "\033[0m"
WHITE = "\033[37m"  # Blanco
PASTEL_YELLOW = "\033[38;5;229m"  # Amarillo pastel
PASTEL_PINK = "\033[38;5;218m"    # Rosa pastel más claro
BOOK = "\U0001F4D6"          # 📖
WRITING_HAND = "\U0000270D"  # ✍️


# Empezamos el scraping

# 1. Obtener el HTML
URL_BASE = 'https://quotes.toscrape.com/'
pedido_obtenido = requests.get(URL_BASE)

# Verificar si la petición fue exitosa
if pedido_obtenido.status_code == 200:
    html_obtenido = pedido_obtenido.text

    # 2. "Parsear" ese HTML
    soup = BeautifulSoup(html_obtenido, "html.parser")

    primer_h1 = soup.find('h1')
    print("\n·················································································\n")
    # Solo el texto limpio y en mayusculas
    primer_h1 = soup.find('h1').text  # Obtener el texto del primer h1
    primer_h1_limpio = re.sub(r'[^a-zA-Z\s]', '', primer_h1)  # Limpiar el texto
    print(f"                              {BOOK}  {primer_h1_limpio.strip().upper()}  {WRITING_HAND}")  # Imprimir en mayúsculas
    print("\n·················································································\n")



    # Iterar sobre cada div con la clase 'quote'
    quotes = soup.find_all('div', class_='quote')
    
    for quote in quotes:
        # Obtener el texto de la cita
        text = quote.find('span', class_='text').text.strip()
        
        # Obtener el autor de la cita
        author = quote.find('small', class_='author').text.strip()
        
        # Limpiar el autor
        cleaned_author = re.sub(r'[^a-zA-Z\s]', '', author).lower().title()
        
        # Obtener las etiquetas de la cita
        tags = quote.find_all('a', class_='tag')
        tag_list = [tag.text.strip().capitalize() for tag in tags]
        
        # Imprimir los resultados
        print(f"{PASTEL_YELLOW}{text}{RESET}")
        print(f"{WHITE}- {cleaned_author}{RESET}")
        print(f"\n{PASTEL_PINK}{' | '.join(tag_list)}{RESET}")
        print("\n·················································································\n")
else:
    print(f"Error al obtener la página. Código de estado: {pedido_obtenido.status_code}")
