import os
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from dotenv import load_dotenv


# Cargar variables de entorno
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Configuración del esquema
db_schema = os.getenv('DB_SCHEMA', 'quotes')  # Valor por defecto si DB_SCHEMA no está definido

metadata = MetaData(schema=db_schema)
Base = declarative_base(metadata=metadata)

# Cadena de conexión 
db_type = os.getenv('DB_TYPE', 'postgresql+asyncpg')
db_host = os.getenv('DB_HOST', 'postgres')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'quotes')
db_user = os.getenv('DB_USER', 'postgres')
db_pass = os.getenv('DB_PASSWORD', 'postgres')

database_url = f"{db_type}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
# print(f"DATA BASE URL: {database_url}")

# Crear motor asíncrono
engine = create_async_engine(database_url, echo=True)

# Crear una clase de sesión asíncrona
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        try:
            # Establecer el search_path al esquema deseado usando SQL raw
            await conn.execute(text(f'SET search_path TO {db_schema}'))
            # Crear todas las tablas definidas por Base.metadata en el esquema
            await conn.run_sync(Base.metadata.create_all)
            print("Base de datos inicializada correctamente.")
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")
            raise

async def shutdown_db():
    # El método dispose no es asíncrono y no necesita ser utilizado en un contexto de async with
    engine.dispose()
    print("Base de datos cerrada correctamente.")
