
![](./assets/logo.jpg)


# SCRAPING QUOTES

¡Te damos la bienvenida a SCRAPING QUOTES!

En XYZ Corp, creemos firmemente en el poder de las palabras para inspirar, motivar y guiar.
 
Buscábamos una frase inspiradora que reflejara, no solo quiénes somos, sino también quiénes aspiramos a ser.

## **WebScraping**

Para alcanzar este objetivo, hemos desarrollado un proyecto innovador que utiliza tecnología de WebScraping en Python.

Utilizando BeautifulSoup, obtenemos frases del sitio web 
#### [quotes.toscrape.com](https://quotes.toscrape.com/)


## **Base de datos**

Mediante las tecnologías PostgreSQL y SQLAlchemy guardamos las frases y su información asociada, en una base de datos, lo cual nos ha permitido examinar minuciosamente cada una de ellas y así seleccionar la mas adecuada.

Este es el esquema UML de las tablas y sus relaciones:

![](./assets/base_de_datos.jpg)

+ **quotes**: Almacena las citas.

Se relaciona con author (cada cita tiene un autor)


+ **author**: Contiene información de los autores.

Se relaciona con birthdate y birthplace (cada autor tiene fecha y lugar de nacimiento)


+ **tags**: Guarda las etiquetas para categorizar citas.

Se relaciona con quotes a través de quote_tags (muchas a muchas)


+ **quote_tag**s: Tabla de unión entre quotes y tags.

Conecta citas con sus etiquetas


+ **birthdate**: Almacena fechas de nacimiento.

Usada por la tabla author


+ **birthplace**: Guarda lugares de nacimiento.

Usada por la tabla author


Esta estructura permite asociar citas con autores, etiquetar citas, y registrar detalles de los autores de manera organizada y eficiente.

## **Docker**

Toda la aplicacion se encuentra dockerizada en tres módulos:

+ Postgres: La base de datos
+ PgAdmin: Plataforma de administración desplegada en http://localhost:5000/
+ App

Los datos de acceso a PgAdmin son:

+ **Usuario:** admin@admin.com
+ **Contraseña:** pgadmin


## **Instalación**

    git clone https://github.com/AI-School-F5-P3/WebScraping_MRosa.git

Navegamos hasta el directorio principal y creamos un entorno virtual
    
    uv venv

Lo activamos

    .venv\Scripts\activate

Ejecutamos el siguiente comando para descargar las dependencias

    uv pip install -r requirements.txt

Necesitaremos crear las variables de entorno en la raíz del proyecto

    DATABASE_URL=postgres://postgres:postgres@postgres:5432/quotes
    DB_TYPE=postgresql+asyncpg
    DB_HOST=postgres 
    DB_PORT=5432

    DB_NAME=quotes
    DB_SCHEMA=quotes

    DB_USER=postgres
    DB_PASSWORD=1234

Podemos iniciar la base de datos localmente en windows ejecutando el archivo **load_env.ps1** de la carpeta /config

En es caso deberemos cambiar en el archivo .env

    DB_HOST=localhost

Para iniciar con Docker ejecutamos

    docker-compose -f docker-compose.yaml up --build                                                                  

## Funcionamiento de la Aplicación de Web Scraping

Esta aplicación de web scraping está diseñada para extraer información de un sitio web, almacenar los datos en una base de datos y ofrecer funcionalidades para mostrar y manejar esta información. Aquí te presento un paso a paso técnico de cómo funciona la aplicación:

### 1. Configuración Inicial

#### Variables de Entorno (.env y config/config.py)

- Las variables de entorno se cargan desde el archivo `.env` utilizando `dotenv`.
- `config/config.py` gestiona la configuración de la aplicación utilizando estas variables.

#### Dependencias (requirements.txt)

- Las dependencias de la aplicación están listadas en `requirements.txt` y se instalan con `pip`.

### 2. Contenedores y Orquestación

#### Docker y Docker Compose (Dockerfile y docker-compose.yaml)

- El `Dockerfile` define la imagen de Docker para el proyecto, incluyendo la instalación de dependencias y la configuración del entorno de ejecución.
- `docker-compose.yaml` orquesta múltiples contenedores Docker, como la aplicación y la base de datos, facilitando el despliegue y la administración.

### 3. Modelado de Datos

#### Definición de Modelos (src/models.py)

- Los modelos de datos se definen utilizando SQLAlchemy. Esto incluye `Birthdate`, `Birthplace`, `Author`, `Tag`, `Quote` y `QuoteTag`.
- Estos modelos representan las tablas en la base de datos y sus relaciones.

### 4. Conexión y Sesión con la Base de Datos

#### Configuración de la Base de Datos (src/database.py y src/utils/conn.py)

- `src/database.py` configura el motor de la base de datos y la sesión asíncrona utilizando SQLAlchemy.
- `src/utils/conn.py` maneja la conexión a la base de datos, utilizando SQLAlchemy y variables de entorno.

### 5. Scraping de Datos

#### Clase Scraper (src/scraper.py)

- `Scraper` es la clase principal responsable del web scraping.
  - `fetch_html`: Obtiene el HTML de una página web utilizando `requests`.
  - `show_header`: Muestra el encabezado de la página.
  - `get_quotes`: Extrae citas de la página utilizando `BeautifulSoup`.
  - `fetch_about_content`: Obtiene información adicional sobre los autores.
  - `display_quotes`: Muestra las citas extraídas.

### 6. Manejo de Citas

#### Clase Quote (src/quote.py)

- `Quote` maneja las operaciones relacionadas con las citas extraídas.
  - `clean_author`: Limpia el nombre del autor.
  - `convert_birthdate`: Convierte la fecha de nacimiento a un formato adecuado.
  - `display`: Muestra las citas con formato.

### 7. Ejecución Principal

#### Script Principal (src/main.py)

- Importa y ejecuta el scraper.
- Utiliza `asyncio` para manejar las operaciones asíncronas.
- Configura el logger para registrar las actividades.

### 8. Utilidades

#### Logger (src/utils/logger.py)

- Configura y maneja el logging con colores para mejorar la legibilidad.
- Utiliza `RotatingFileHandler` para manejar los archivos de log.

#### Loader (src/utils/loader.py)

- Implementa un cargador animado en segundo plano para indicar el progreso de las operaciones.

#### Constantes (src/utils/constants.py)

- Define constantes utilizadas en toda la aplicación, como URLs, headers y colores para el formato de salida.

### 9. Inicialización de la Base de Datos

#### Script SQL (initdb/init.sql)

- Contiene comandos SQL para inicializar la base de datos con las tablas y datos necesarios.

## Flujo de Trabajo

### Inicialización

- Carga las variables de entorno.
- Configura la base de datos y establece la conexión.

#### Web Scraping

- El scraper se ejecuta, obtiene el HTML de las páginas objetivo y extrae las citas y la información adicional.

#### Almacenamiento

- Las citas y la información asociada se almacenan en la base de datos utilizando los modelos definidos.

### Visualización

- Las citas almacenadas se pueden mostrar en la terminal o exportar según sea necesario.

### Logging y Monitoreo

- Toda la actividad se registra para monitoreo y depuración.

Esta aplicación es modular y extensible, permitiendo que nuevas funcionalidades se añadan fácilmente. El uso de contenedores Docker garantiza que sea portable y fácil de desplegar en diferentes entornos.

## **Conclusión**

Este proyecto no solo es un esfuerzo por encontrar una frase inspiradora, sino una demostración de cómo podemos utilizar la tecnología para mejorar y enriquecer nuestra identidad corporativa. Estamos entusiasmados por el potencial de este proyecto y confiamos en que el resultado será una frase que todos en XYZ Corp podamos abrazar con orgullo y que inspire a todos aquellos con los que interactuamos.