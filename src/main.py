from bs4 import BeautifulSoup
import requests
import re
import constants


# User-Agent para protegernos de baneos
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
URL_BASE = 'https://quotes.toscrape.com/'
response = requests.get(URL_BASE, headers=headers) # Obtener el HTML

# Verificar si la petición fue exitosa
if response.status_code == 200:
    html = response.text

    # "Parsear" ese HTML
    soup = BeautifulSoup(html, "html.parser")

    primer_h1 = soup.find('h1')
    print(constants.separator)
    # Solo el texto limpio y en mayusculas
    primer_h1 = soup.find('h1').text  # Obtener el texto del primer h1
    primer_h1_limpio = re.sub(r'[^a-zA-Z\s]', '', primer_h1)  # Limpiar el texto
    print(f"                              {constants.BOOK}  {primer_h1_limpio.strip().upper()}  {constants.WRITING_HAND}")  # Imprimir en mayúsculas
    print(constants.separator)



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
        print(f"{constants.PASTEL_YELLOW}{text}{constants.RESET}")
        print(f"{constants.WHITE}- {cleaned_author}{constants.RESET}")
        print(f"\n{constants.PASTEL_PINK}{' | '.join(tag_list)}{constants.RESET}")
        print(constants.separator)
else:
    print(f"Error al obtener la página. Código de estado: {response.status_code}")
