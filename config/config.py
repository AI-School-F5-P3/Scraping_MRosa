import os
from dotenv import main

# Cargar las variables de entorno del archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
main.load_dotenv(dotenv_path)

# Acceder a las variables de entorno
database_url = os.getenv('DATABASE_URL')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
secret_key = os.getenv('SECRET_KEY')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
debug_mode = os.getenv('DEBUG')

print(f"Database URL: {database_url}")
print(f"Database Host: {db_host}")
print(f"Database Port: {db_port}")
print(f"Database Name: {db_name}")
print(f"Secret Key: {secret_key}")
print(f"User: {db_user}")
print(f"Secret password: {db_pass}")
print(f"Debug Mode: {debug_mode}")
