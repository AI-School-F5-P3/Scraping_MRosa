from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
import asyncio

import os
from dotenv import main
from constants import  GREEN, RED, RESET  # Importa constantes de formato desde el módulo 'constants'.


main.load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Crea una instancia de declarative_base
Base = declarative_base()

# Cadena de conexión 
# Acceder a las variables de entorno

db_type = os.getenv('DB_TYPE')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_DB')
db_schema = os.getenv('DB_SCHEMA')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')

DATABASE_URL = f"{db_type}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
print(DATABASE_URL)

async def test_connection():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        try:
            result = await session.execute(text("SELECT 1"))
            print(f"{result}\n\n{GREEN}Conexión exitosa!\n{RESET}{DATABASE_URL}\n\n")
        except Exception as e:
            print(f"n{RED}Error al conectar:{RESET} {e}")

asyncio.run(test_connection())
