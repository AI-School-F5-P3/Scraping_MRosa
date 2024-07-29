import sys
import os
# Añade el directorio raíz al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from dotenv import main
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from sqlalchemy.exc import OperationalError  # Para manejar errores de conexión
from src.utils.constants import PASTEL_YELLOW, GREEN, PASTEL_PINK, RED_CIRCLE, RED, RESET  # Importa constantes de formato desde el módulo 'constants'.


# Cargar variables de entorno desde el archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
main.load_dotenv(dotenv_path)

# Crear una base de datos declarativa
Base = declarative_base()

# Función para establecer la conexión a la base de datos
async def connect_to_database():
    try:
        db_type = os.getenv('DB_TYPE')
        db_host = 'localhost'
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_pass = os.getenv('DB_PASSWORD')

        # Construir la URL de conexión
        database_url = f"{db_type}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        print(f"\n{PASTEL_PINK}Conectando a: {PASTEL_YELLOW}{database_url}{RESET}\n")

        # Crear el motor de base de datos asíncrono
        engine = create_async_engine(database_url, echo=True)

        # Crear una sesión asíncrona
        async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

        # Probar la conexión ejecutando una consulta simple
        async with async_session() as session:
            result = await session.execute(text("SELECT 1"))
            print(f"\n{result}\n")
            print(f"{GREEN}\nConexión exitosa a: {PASTEL_YELLOW} {database_url}{RESET}\n")
            return engine, async_session

    except OperationalError as e:
        print(f"\n{RED_CIRCLE} {RED}Error al conectar a la base de datos: {PASTEL_YELLOW} {e}{RESET}\n")
    except Exception as e:
        print(f"\n{RED_CIRCLE} {RED}Error inesperado:{RESET} {e}\n")
    return None, None

# Función principal para ejecutar la conexión
async def main():
    await connect_to_database()


# Ejecutar el bucle de eventos de asyncio
asyncio.run(main())