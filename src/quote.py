import sys
import os
# Añade el directorio raíz al sys.path para que se pueda importar desde otros módulos en la jerarquía de directorios superior.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re  # Importa el módulo 're' para trabajar con expresiones regulares.
from datetime import datetime  # Importa la clase datetime para manejar fechas y horas.
from sqlalchemy.ext.asyncio import AsyncSession  # Importa 'AsyncSession' para manejar sesiones asíncronas de SQLAlchemy.
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
            birthdate (str): La fecha de nacimiento del autor en formato 'Month day, Year'.
            tag_list (list of str): Etiquetas asociadas con la cita.
            birthplace (str): El lugar de nacimiento del autor.
            description (str): Una descripción adicional del autor.
        '''
        try:
            self.text = str(text)  # Convierte y asigna el texto de la cita a un atributo de instancia.
            self.author = self.clean_author(author)  # Limpia y asigna el nombre del autor usando el método estático.
            self.birthdate = self.convert_birthdate(birthdate)  # Convierte la fecha de nacimiento desde 'Month day, Year' a 'dd-mm-yyyy'.
            self.birthplace = str(birthplace)  # Convierte y asigna el lugar de nacimiento.
            self.description = str(description)  # Convierte y asigna la descripción.
            self.tags = list(tag_list)  # Convierte y asigna la lista de etiquetas.
        except Exception as e:  
            logger.error(f"Error al inicializar Quote: {e}")  
            raise  # Lanza nuevamente la excepción para que sea manejada en un nivel superior.

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
            return re.sub(r'[^a-zA-Z\s]', '', author).lower().title()  # Usa expresiones regulares para limpiar y formatear el nombre.
        except Exception as e:  
            logger.error(f"Error al limpiar el nombre del autor: {e}")  
            return (f"{RED}Error{RESET}")  

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
        except ValueError as ve:  # Captura excepciones de tipo ValueError que pueden ocurrir si el formato de la fecha es incorrecto.
            logger.error(f"Error al analizar la fecha de nacimiento: {birthdate_str} - {ve}")  
            raise  # Lanza la excepción para ser manejada en un nivel superior.

    def display(self):
        '''
        Muestra la cita, el autor y las etiquetas en un formato estilizado.
        '''
        try:
            print(f"{PASTEL_YELLOW}{self.text}{RESET}\n")  # Imprime el texto de la cita en color amarillo pastel.
            print(f"{WHITE}{self.author} ({self.birthdate} {self.birthplace}) {RESET}\n")  # Imprime el autor, fecha y lugar de nacimiento en blanco.
            print(f"{WHITE}{self.description}{RESET}")  # Imprime la descripción en blanco.
            print(f"\n{PASTEL_PINK}{' | '.join(self.tags)}{RESET}")  # Imprime las etiquetas en color rosa pastel, separadas por ' | '.
            print(SEPARATOR)  # Imprime un separador.
            print("")  # Imprime una línea en blanco.
        except Exception as e:  # Captura cualquier excepción que ocurra durante la visualización.
            logger.error(f"Error al mostrar la cita: {e}")  

    async def _insert_birthdate(self, session: AsyncSession):
        """Inserta la fecha de nacimiento en la base de datos."""
        try:
            # El atributo self.birthdate ya es un objeto datetime.date
            result = await session.execute(
                select(Birthdate).filter_by(birthdate=self.birthdate)  # Realiza una consulta para obtener la fecha de nacimiento.
            )
            bdate = result.scalars().first()  # Obtiene el primer resultado de la consulta.
            if not bdate:  # Si no existe la fecha de nacimiento, crea una nueva instancia.
                bdate = Birthdate(birthdate=self.birthdate)
                session.add(bdate)  # Agrega la nueva fecha de nacimiento a la sesión.
                await session.flush()  # Realiza un flush de la sesión para sincronizar con la base de datos.
            return bdate  # Devuelve la fecha de nacimiento.
        except Exception as e:  
            logger.error(f"Error al manejar la fecha de nacimiento: {e}")  
            raise  # Lanza nuevamente la excepción para ser manejada en un nivel superior.

    async def _insert_birthplace(self, session: AsyncSession):
        """Inserta el lugar de nacimiento en la base de datos."""
        try:
            result = await session.execute(
                select(Birthplace).filter_by(birthplace=self.birthplace)  # Realiza una consulta para obtener el lugar de nacimiento.
            )
            place = result.scalars().first()  # Obtiene el primer resultado de la consulta.
            if not place:  # Si no existe el lugar de nacimiento, crea una nueva instancia.
                place = Birthplace(birthplace=self.birthplace)
                session.add(place)  # Agrega el nuevo lugar de nacimiento a la sesión.
                await session.flush()  # Realiza un flush de la sesión para sincronizar con la base de datos.
            return place  # Devuelve el lugar de nacimiento.
        except Exception as e:  
            logger.error(f"Error al manejar el lugar de nacimiento: {e}")  
            raise  # Lanza nuevamente la excepción para ser manejada en un nivel superior.

    async def _insert_author(self, session: AsyncSession):
        """Inserta el autor en la base de datos."""
        bdate = await self._insert_birthdate(session)  # Inserta la fecha de nacimiento.
        place = await self._insert_birthplace(session)  # Inserta el lugar de nacimiento.

        result = await session.execute(
            select(Author).filter_by(name=self.author)  # Realiza una consulta para obtener el autor.
        )
        author = result.scalars().first()  # Obtiene el primer resultado de la consulta.
        if not author:  # Si no existe el autor, crea una nueva instancia de Author.
            author = Author(name=self.author, birthdate_id=bdate.id, birthplace_id=place.id, description=self.description)
            session.add(author)  # Agrega el nuevo autor a la sesión.
            await session.flush()  # Realiza un flush de la sesión para sincronizar con la base de datos.
        return author  # Devuelve el autor.

    async def _insert_tags(self, session: AsyncSession):
        """Inserta las etiquetas en la base de datos."""
        try:
            tag_ids = []  # Lista para almacenar los IDs de las etiquetas.
            for my_tag in self.tags:  # Itera sobre cada etiqueta en la lista de etiquetas.
                result = await session.execute(
                    select(Tag).filter_by(tag=my_tag)  # Realiza una consulta para obtener la etiqueta.
                )
                tag = result.scalars().first()  # Obtiene el primer resultado de la consulta.
                if not tag:  # Si no existe la etiqueta, crea una nueva instancia.
                    tag = Tag(tag=my_tag)
                    session.add(tag)  # Agrega la nueva etiqueta a la sesión.
                    await session.flush()  # Realiza un flush de la sesión para sincronizar con la base de datos.
                tag_ids.append(tag.id)  # Agrega el ID de la etiqueta a la lista.
            return tag_ids  # Devuelve la lista de IDs de las etiquetas.
        except Exception as e:  
            logger.error(f"Error al manejar las etiquetas: {e}")  
            raise  # Lanza nuevamente la excepción para ser manejada en un nivel superior.

    async def _insert_quote(self, session: AsyncSession):
        """Guarda la cita en la base de datos."""
        try:
            author = await self._insert_author(session)  # Inserta el autor.
            db_quote = DBQuote(quote=self.text, author_id=author.id)  # Crea una nueva instancia de DBQuote con el texto y el ID del autor.
            session.add(db_quote)  # Agrega la nueva cita a la sesión.
            await session.flush()  # Realiza un flush de la sesión para sincronizar con la base de datos.
        except Exception as e:  
            logger.error(f"Error al guardar la cita en la base de datos: {e}, {type(e)}")  
            await session.rollback()  # Realiza un rollback de la sesión para deshacer cualquier cambio realizado.

    async def save(self, session: AsyncSession):
        """Guarda la cita en la base de datos, incluyendo etiquetas."""
        try:
            await self._insert_quote(session)  # Guarda la cita en la base de datos.
            tag_ids = await self._insert_tags(session)  # Inserta las etiquetas y obtiene sus IDs.

            # Obtener la cita recién insertada
            result = await session.execute(
                select(DBQuote).filter_by(quote=self.text)  # Realiza una consulta para obtener la cita.
            )
            quote = result.scalars().first()  # Obtiene el primer resultado de la consulta.

            # Asociar las etiquetas con la cita
            for tag_id in tag_ids:  # Itera sobre cada ID de etiqueta.
                quote_tags = QuoteTag(quote_id=quote.id, tag_id=tag_id)  # Crea una instancia de QuoteTag para asociar la etiqueta con la cita.
                session.add(quote_tags)  # Agrega la asociación a la sesión.

            await session.flush()  # Realiza un flush de la sesión para sincronizar con la base de datos.
            await session.commit()  # Realiza un commit de la sesión para persistir los cambios.
        except Exception as e:  
            logger.error(f"Error al guardar la cita en la base de datos: {e}")  
            await session.rollback()  # Realiza un rollback de la sesión para deshacer cualquier cambio realizado.
