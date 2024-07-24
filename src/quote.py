import re
from logger import logger
from constants import SEPARATOR, PASTEL_YELLOW, PASTEL_PINK, WHITE, RED, RESET

class Quote:
    '''
    Representa una cita con un texto, autor y etiquetas asociadas.\n
    La clase `Quote` permite almacenar y mostrar una cita. Además, incluye un método estático para limpiar el nombre del autor
    eliminando caracteres no alfabéticos y capitalizando adecuadamente el nombre.

    Atributos:
        text (str): El texto de la cita.
        author (str): El autor de la cita, procesado para eliminar caracteres no alfabéticos y formateado.
        tags (list of str): Etiquetas asociadas con la cita.

    Métodos:
        clean_author(author):
            Limpia y formatea el nombre del autor eliminando caracteres no alfabéticos y capitalizando el nombre.\n
        display():
            Imprime la cita, el autor y las etiquetas en un formato estilizado.
    '''

    def __init__(self, text, author, born_date, tag_list, born_location, description):
        '''
        Inicializa una instancia de la clase Quote.\n
        Args:
            text (str): El texto de la cita.
            author (str): El autor de la cita.
            tags (list of str): Etiquetas asociadas con la cita.
        '''
        try:
            self.text = str(text)
            self.author = self.clean_author(author)
            self.born_date = str(born_date)
            self.born_location = str(born_location)
            self.description = str(description)
            
            self.tags = list(tag_list)
            


            # # Separar la self.about_content por comas
            # lista_frutas = self.about_content.split('in')
            # print(f"lista_frutas {lista_frutas}")

            # # Asignar cada elemento a una variable
            # self.title, self.born_date, self.born_location, self.description = lista_frutas

            # # Verificar si la longitud es la esperada
            # if len(lista_frutas) == 4:
            #     # Asignar cada elemento a una variable
            #     self.title, self.born_date, self.born_location, self.description = lista_frutas
            # else:
            #     raise ValueError(f"Se esperaban 4 elementos en 'about_content', pero se encontraron {len(lista_frutas)}")

            # # Imprimir las variables
            # print(self.title)
            # print(self.born_date)
            # print(self.born_location)
            # print(self.description)
        except Exception as e:
            logger.error(f"Error al inicializar Quote: {e}")
            raise # Indicamos que este es un error que no podemos manejar completamente en este nivel y que debe ser manejado por el código que está intentando crear la instancia de Quote

    '''
    El decorador @staticmethod en Python se utiliza para definir un método estático dentro de una clase. 
    Un método estático no recibe automáticamente una referencia a la instancia de la clase (normalmente self) ni a la clase en sí (normalmente cls). En su lugar, funciona como una función regular que simplemente reside en el espacio de nombres de la clase. Esto es útil cuando tienes un método que no necesita acceder ni modificar el estado de la instancia ni de la clase.
    En el contexto de la clase Quote, el método clean_author se define como estático porque su operación (limpiar el nombre del autor) no depende de ninguna propiedad de la instancia de la clase Quote. 
    '''
    @staticmethod
    def clean_author(author):
        '''
        Limpia y formatea el nombre del autor.

        Elimina todos los caracteres no alfabéticos y convierte el nombre a un formato capitalizado.

        Args:
            author (str): El nombre del autor a limpiar.

        Returns:
            str: El nombre del autor limpio y capitalizado.
        '''
        try:
            return re.sub(r'[^a-zA-Z\s]', '', author).lower().title()
        except Exception as e:
            logger.error(f"Error al limpiar el nombre del autor: {e}")
            return (f"{RED}Error{RESET}")

    def display(self):
        '''
        Muestra la cita, el autor y las etiquetas en un formato estilizado.
        '''
        try:
            print(f"{PASTEL_YELLOW}{self.text}{RESET}\n")
            print(f"{WHITE}{self.author} ({self.born_date} {self.born_location}) {RESET}\n")
            # print(f"{WHITE}{self.description}{RESET}")
            print(f"\n{PASTEL_PINK}{' | '.join(self.tags)}{RESET}")
            print(SEPARATOR)
        except Exception as e:
            logger.error(f"Error al mostrar la cita: {e}")