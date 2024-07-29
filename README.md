
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

    - Se relaciona con author (cada cita tiene un autor)


+ **author**: Contiene información de los autores.

    - Se relaciona con birthdate y birthplace (cada autor tiene fecha y lugar de nacimiento)


+ **tags**: Guarda las etiquetas para categorizar citas.

    - Se relaciona con quotes a través de quote_tags (muchas a muchas)


+ **quote_tag**s: Tabla de unión entre quotes y tags.

    - Conecta citas con sus etiquetas


+ **birthdate**: Almacena fechas de nacimiento.

    - Usada por la tabla author


+ **birthplace**: Guarda lugares de nacimiento.

    - Usada por la tabla author


Esta estructura permite asociar citas con autores, etiquetar citas, y registrar detalles de los autores de manera organizada y eficiente.

## **Docker**

Toda la aplicacion se encuentra dockerizada en tres módulos:

+ **Postgres:** La base de datos
+ **PgAdmin:** Plataforma de administración desplegada en http://localhost:5000/
+ **App** App en Python

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

Esta aplicación de web scraping está diseñada para extraer información de un sitio web y almacenar los datos en una base de datos. 

Aquí presentamos un paso a paso técnico de cómo funciona la aplicación:

### 1. Configuración Inicial

#### Variables de Entorno (.env y config/config.py)

- Las variables de entorno se cargan desde el archivo `.env` utilizando `dotenv`.
- `config/config.py` verifica la configuración de la aplicación utilizando estas variables.

#### Base de datos
- `config/conn.py` verifica la conexión a la base de datos local con las variables de entorno.

#### Dependencias (requirements.txt)

- Las dependencias de la aplicación están listadas en `requirements.txt`.

### 2. Contenedores y Orquestación

#### Docker y Docker Compose (Dockerfile y docker-compose.yaml)

+ El `Dockerfile` define la imagen de Docker para el proyecto, incluyendo la instalación de dependencias y la configuración del entorno de ejecución.
+ `docker-compose.yaml` orquesta múltiples contenedores Docker, como la aplicación y la base de datos, facilitando el despliegue y la administración.

### 3. Modelado de Datos

#### Definición de Modelos (src/models.py)

+ Los modelos de datos se definen utilizando SQLAlchemy. Esto incluye `Birthdate`, `Birthplace`, `Author`, `Tag`, `Quote` y `QuoteTag`.
+ Estos modelos representan las tablas en la base de datos y sus relaciones.

### 4. Conexión y Sesión con la Base de Datos

#### Configuración de la Base de Datos (src/database.py y src/utils/conn.py)

+ `src/database.py` configura el motor de la base de datos y la sesión asíncrona utilizando SQLAlchemy y variables de entorno.

### 5. Scraping de Datos

#### Clase Scraper (src/scraper.py)

La clase `Scraper` se utiliza para realizar web scraping y extraer las citas junto con la información relacionada de los autores.


+ **Importaciones**: 
    - Módulos y clases necesarios para realizar scraping, procesar HTML, manejar excepciones y trabajar con la base de datos.
+ **Configuraciones y Constantes**:
    - Importación de constantes y configuraciones específicas desde `src.utils.constants`.


+ **Atributos**

    - `soups`: Lista para almacenar objetos `BeautifulSoup` que contienen el HTML de cada página web.

    - `header_shown`: Controla si el encabezado H1 ya ha sido mostrado (no utilizado en el código proporcionado).

+ **Métodos**

1. **`__init__(self)`**: Inicializa la clase.

2. **`fetch_html(self)`**: 
   - Obtiene el HTML de las páginas web especificadas en un rango de páginas.
   - Almacena los objetos `BeautifulSoup` en la lista `soups`.

3. **`has_data(self, soup)`**: 
   - Verifica si la página contiene datos relevantes.

4. **`show_header(self, soup)`**:
   - Muestra el primer encabezado H1 de la página web.

5. **`get_quotes(self)`**:
   - Extrae citas de todas las páginas web almacenadas en `soups`.
   - Devuelve una lista de objetos `Quote`.

6. **`fetch_about_content(self, about_url)`**:
   - Realiza una solicitud HTTP para obtener el contenido de la página "about".
   - Extrae y devuelve información sobre el autor.

7. **`display_quotes(self, quotes_list)`**:
   - Muestra en pantalla las citas contenidas en `quotes_list`.

8. **`save_quotes_to_db(self, quotes_list)`**:
   - Guarda todas las citas en una base de datos.
   - Utiliza una sesión asincrónica para guardar cada cita.

+ **Notas Adicionales**

    - **Logger**: Se utiliza `logger` para registrar errores y eventos importantes.
    - **Manejo de Excepciones**: Implementación de bloques `try-except` para manejar errores durante el procesamiento de datos.


### 6. Manejo de Citas

#### Clase Quote (src/quote.py)

Este archivo define una clase `Quote` utilizada para representar una cita con su texto, autor, etiquetas asociadas y métodos para manipular y almacenar estos datos en una base de datos asíncrona.

+ **Importaciones y Configuración Inicial**

   - Módulos para trabajar con expresiones regulares (`re`) y fechas (`datetime`).
   - Herramientas de SQLAlchemy para manejar sesiones asíncronas y realizar consultas.
   - Modelos de base de datos desde `models` (Author, Quote, Tag, QuoteTag, Birthdate, Birthplace).
   - Objeto `logger` para registrar mensajes de error.
   - Constantes de formato desde `src.utils.constants`.

+ **Atributos**

    - `text`: El texto de la cita.
    - `author`: El autor de la cita, procesado para eliminar caracteres no alfabéticos y formateado.
    - `birthdate`: La fecha de nacimiento del autor, convertida a un objeto `datetime.date`.
    - `birthplace`: El lugar de nacimiento del autor.
    - `description`: Descripción adicional del autor.
    - `tags`: Lista de etiquetas asociadas con la cita.

+ **Métodos**

1. **`__init__(self, text, author, birthdate, tag_list, birthplace, description)`**:
   - Inicializa una instancia de la clase `Quote`.

2. **`clean_author(author)`**:
   - Limpia y formatea el nombre del autor eliminando caracteres no alfabéticos y capitalizando el nombre.

3. **`convert_birthdate(birthdate_str)`**:
   - Convierte una fecha de nacimiento desde el formato 'Month day, Year' a un objeto `datetime.date`.

4. **`display(self)`**:
   - Muestra la cita, el autor, las etiquetas, la fecha de nacimiento y el lugar de nacimiento en un formato estilizado.

5. **`_insert_birthdate(self, session: AsyncSession)`**:
   - Inserta la fecha de nacimiento en la base de datos.

6. **`_insert_birthplace(self, session: AsyncSession)`**:
   - Inserta el lugar de nacimiento en la base de datos.

7. **`_insert_author(self, session: AsyncSession)`**:
   - Inserta el autor en la base de datos.

8. **`_insert_tags(self, session: AsyncSession)`**:
   - Inserta las etiquetas en la base de datos.

9. **`_insert_quote(self, session: AsyncSession)`**:
   - Guarda la cita en la base de datos.

10. **`save(self, session: AsyncSession)`**:
    - Guarda la cita en la base de datos, incluyendo etiquetas y asociaciones con el autor.

### 7. Ejecución Principal

#### Script Principal (src/main.py)

La función principal `main` realiza las siguientes acciones:

1. **Crear una instancia de la clase `Scraper`**:
   - Se utiliza para gestionar el proceso de scraping.

2. **Obtener el HTML de la página web**:
   - Llama al método `fetch_html` de `Scraper` para obtener y almacenar el HTML de la página web en el atributo `soup`.

3. **Extraer las citas de la página web**:
   - Llama al método `get_quotes` de `Scraper` para extraer una lista de citas desde la página web.

4. **Guardar las citas en la base de datos**:
   - Llama al método `save_quotes_to_db` de `Scraper` para guardar las citas extraídas en la base de datos.

5. **Manejo de excepciones**:
   - Captura cualquier excepción inesperada que ocurra durante el flujo principal y registra un mensaje de error.

### 8. Utilidades

#### Logger (src/utils/logger.py)

- Configura y maneja el logging con colores para mejorar la legibilidad.
- Utiliza `RotatingFileHandler` para manejar los archivos de log.

#### Loader (src/utils/loader.py)

- Implementa un cargador animado en segundo plano para indicar el progreso de las operaciones (Se ha comentado para la implementacion en Docker, ya que no se visualiza).

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

### Logging y Monitoreo

- Toda la actividad se registra para monitoreo y depuración.

Esta aplicación es modular y extensible, permitiendo que nuevas funcionalidades se añadan fácilmente. El uso de contenedores Docker garantiza que sea portable y fácil de desplegar en diferentes entornos.

## **Conclusión**

Este proyecto no solo es un esfuerzo por encontrar una frase inspiradora, sino una demostración de cómo podemos utilizar la tecnología para mejorar y enriquecer nuestra identidad corporativa. Estamos entusiasmados por el potencial de este proyecto y confiamos en que el resultado será una frase que todos en XYZ Corp podamos abrazar con orgullo y que inspire a todos aquellos con los que interactuamos.
