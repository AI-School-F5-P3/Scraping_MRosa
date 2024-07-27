import sys
import os
# Añade el directorio raíz al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re  # Importa el módulo 're' para trabajar con expresiones regulares.
from datetime import datetime  # Asegúrate de que esta línea esté presente
from sqlalchemy.ext.asyncio import AsyncSession  # Importa 'AsyncSession' para trabajar con sesiones asíncronas de SQLAlchemy.
from sqlalchemy.future import select  # Importa 'select' para realizar consultas de SQLAlchemy.
from models import Author, Quote as DBQuote, Tag, QuoteTag, Birthdate, Birthplace  # Importa modelos de la base de datos desde el módulo 'models'.
from src.utils.logger import logger  # Importa el objeto 'logger' del módulo 'logger' para registrar mensajes de error.
from src.utils.constants import SEPARATOR, PASTEL_YELLOW, PASTEL_PINK, WHITE, RED, RESET  # Importa constantes de formato desde el módulo 'constants'.




class Quote:
    '''
    Representa una cita con un texto, autor y etiquetas asociadas.
    La clase `Quote` permite almacenar y mostrar una cita. Además, incluye un método estático para limpiar el nombre del autor
    eliminando caracteres no alfabéticos y capitalizando adecuadamente el nombre.

    Atributos:
        text (str): El texto de la cita.
        author (str): El autor de la cita, procesado para eliminar caracteres no alfabéticos y formateado.
        tags (list of str): Etiquetas asociadas con la cita.

    Métodos:
        clean_author(author):
            Limpia y formatea el nombre del autor eliminando caracteres no alfabéticos y capitalizando el nombre.
        display():
            Imprime la cita, el autor y las etiquetas en un formato estilizado.
    '''

    def __init__(self, text, author, birthdate, tag_list, birthplace, description):
        '''
        Inicializa una instancia de la clase Quote.
        Args:
            text (str): El texto de la cita.
            author (str): El autor de la cita.
            tags (list of str): Etiquetas asociadas con la cita.
        '''
        try:
            self.text = str(text)  # Convierte y asigna el texto de la cita a un atributo de instancia.
            self.author = self.clean_author(author)  # Limpia y asigna el nombre del autor usando el método estático.
            # Convierte la fecha de nacimiento desde 'Month day, Year' a 'dd-mm-yyyy'
            self.birthdate = self.convert_birthdate(birthdate)  # Guardamos la fecha en formato 'dd-mm-yyyy'
            self.birthplace = str(birthplace)  # Convierte y asigna el lugar de nacimiento.
            self.description = str(description)  # Convierte y asigna la descripción.
            
            self.tags = list(tag_list)  # Convierte y asigna la lista de etiquetas.
 
        except Exception as e:  # Captura cualquier excepción que ocurra durante la inicialización.
            logger.error(f"Error al inicializar Quote: {e}")  # Registra el error.
            raise  # Lanza nuevamente la excepción para que sea manejada en un nivel superior.

    '''
    El decorador @staticmethod en Python se utiliza para definir un método estático dentro de una clase. 
    Un método estático no recibe automáticamente una referencia a la instancia de la clase (normalmente self) ni a la clase en sí (normalmente cls). En su lugar, funciona como una función regular que simplemente reside en el espacio de nombres de la clase. Esto es útil cuando tienes un método que no necesita acceder ni modificar el estado de la instancia ni de la clase.
    En el contexto de la clase Quote, el método clean_author se define como estático porque su operación (limpiar el nombre del autor) no depende de ninguna propiedad de la instancia de la clase Quote. 
    '''
    @staticmethod  # Define un método estático que no depende de la instancia de la clase.
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
            return re.sub(r'[^a-zA-Z\s]', '', author).lower().title()  # Usa expresiones regulares para limpiar y formatear el nombre.
        except Exception as e:  # Captura cualquier excepción que ocurra durante la limpieza.
            logger.error(f"Error al limpiar el nombre del autor: {e}")  # Registra el error.
            return (f"{RED}Error{RESET}")  # Devuelve una cadena indicando un error.

    @staticmethod
    def convert_birthdate(birthdate_str):
        '''
        Convierte una fecha de nacimiento desde el formato 'Month day, Year' a un objeto datetime.date.
        
        Args:
            birthdate_str (str): La fecha de nacimiento en formato 'Month day, Year'.

        Returns:
            datetime.date: La fecha de nacimiento convertida.
        '''
        try:
            # Convertir la cadena de fecha a un objeto datetime.date
            birthdate_obj = datetime.strptime(birthdate_str, '%B %d, %Y').date()
            return birthdate_obj
        
        except ValueError as ve:
            logger.error(f"Error al analizar la fecha de nacimiento: {birthdate_str} - {ve}")
            raise

    def display(self):
        '''
        Muestra la cita, el autor y las etiquetas en un formato estilizado.
        '''
        try:
            print(f"{PASTEL_YELLOW}{self.text}{RESET}\n")  # Comentado: imprime el texto de la cita en color amarillo pastel.
            print(f"{WHITE}{self.author} ({self.birthdate} {self.birthplace}) {RESET}\n")  # Imprime el autor, fecha y lugar de nacimiento en blanco.
            print(f"{WHITE}{self.description}{RESET}")  # Comentado: imprime la descripción en blanco.
            print(f"\n{PASTEL_PINK}{' | '.join(self.tags)}{RESET}")  # Comentado: imprime las etiquetas en color rosa pastel, separadas por ' | '.
            print(SEPARATOR)  # Comentado: imprime un separador.
            print("")
        except Exception as e:  # Captura cualquier excepción que ocurra durante la visualización.
            logger.error(f"Error al mostrar la cita: {e}")  # Registra el error.

    async def _insert_birthdate(self, session: AsyncSession):
        """Obtiene o crea la fecha de nacimiento."""
        try:
            # El atributo self.birthdate ya es un objeto datetime.date
            result = await session.execute(
                select(Birthdate).filter_by(birthdate=self.birthdate)
            )
            bdate = result.scalars().first()
            if not bdate:
                bdate = Birthdate(birthdate=self.birthdate)
                session.add(bdate)
                await session.flush()
            return bdate
        except Exception as e:
            logger.error(f"Error al manejar la fecha de nacimiento: {e}")
            raise
    
    async def _insert_birthplace(self, session: AsyncSession):
        """Obtiene o crea la fecha de nacimiento."""
        try:
            # El atributo self.birthplace ya es un objeto datetime.date
            result = await session.execute(
                select(Birthplace).filter_by(birthplace=self.birthplace)
            )
            place = result.scalars().first()

            if not place:
                place = Birthplace(birthplace=self.birthplace)
                session.add(place)
                await session.flush()
            return place
        except Exception as e:
            logger.error(f"Error al manejar el lugar de nacimiento: {e}")
            raise

    async def _create_author(self, session: AsyncSession):
        """Obtiene o crea el autor en la base de datos."""
        bdate = await self._insert_birthdate(session)  # Insertar la fecha de nacimiento
        place = await self._insert_birthplace(session)  # Insertar el lugar de nacimiento

        result = await session.execute(
            select(Author).filter_by(name=self.author)  # Realiza una consulta para obtener el autor.
        )
        author = result.scalars().first()  # Obtiene el primer resultado de la consulta.
        if not author:  # Si no existe, crea una nueva instancia de Author.
            author = Author(name=self.author, birthdate_id=bdate.id, birthplace_id=place.id, description=self.description)
            session.add(author)  # Agrega el nuevo autor a la sesión.
            await session.flush()  # Realiza un flush de la sesión para sincronizar con la base de datos.
        return author  # Devuelve el autor.

    async def _insert_tags(self, session: AsyncSession):
        """Inserta los tags"""
        try:
            tag_ids = []
            for my_tag in self.tags:
                result = await session.execute(
                    select(Tag).filter_by(tag=my_tag)
                )
                tag = result.scalars().first()
                if not tag:
                    tag = Tag(tag=my_tag)
                    session.add(tag)
                    await session.flush()
                tag_ids.append(tag.id)
            return tag_ids
        except Exception as e:
            logger.error(f"Error al manejar las etiquetas: {e}")
            raise

        

    async def _insert_quote(self, session: AsyncSession):
        """Guarda la cita en la base de datos."""
        try:
            author = await self._create_author(session)             
            db_quote = DBQuote(quote=self.text, author_id=author.id)
            session.add(db_quote)
            await session.flush()
            # await session.commit()
        except Exception as e:
            logger.error(f"Error al guardar la cita en la base de datos: {e}, {type(e)}")
            await session.rollback()


    async def save(self, session: AsyncSession):
        """Guarda la cita en la base de datos."""
        try:
            await self._insert_quote(session)
            tag_ids = await self._insert_tags(session)

            # Obtener la cita recién insertada
            result = await session.execute(
                select(DBQuote).filter_by(quote=self.text)
            )
            quote = result.scalars().first()

            # Asociar las etiquetas con la cita
            for tag_id in tag_ids:
                quote_tags = QuoteTag(quote_id=quote.id, tag_id=tag_id)
                session.add(quote_tags)
            
            await session.flush()
            await session.commit()
        except Exception as e:
            logger.error(f"Error al guardar la cita en la base de datos: {e}")
            await session.rollback()


    