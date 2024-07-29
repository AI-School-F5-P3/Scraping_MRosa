# SCRAPING QUOTES

:grinning: ¡Te damos la bienvenida a SCRAPING QUOTES!

## Introducción

En XYZ Corp, creemos firmemente en el poder de las palabras para inspirar, motivar y guiar.
 
Buscábamos una frase inspiradora que reflejara, no solo quiénes somos, sino también quiénes aspiramos a ser.

## Objetivos del Proyecto

**WebScraping**
Para alcanzar este objetivo, hemos desarrollado un proyecto innovador que utiliza tecnología de Web Scraping en Python.

Utilizando BeautifulSoup, obtenemos frases del sitio web 
#### [quotes.toscrape.com](https://quotes.toscrape.com/)

**Base de datos**
Mediante las tecnologías PostgreSQL y SQLAlchemy guardamos las frases y su información asociada, en una base de datos, lo cual nos ha permitido examinar minuciosamente cada una de ellas y así seleccionar la mas adecuada.

Este es el esquema UML de las tablas y sus relaciones:

![](./assets/header.jpg)

quotes: Almacena las citas.

Se relaciona con author (cada cita tiene un autor)


author: Contiene información de los autores.

Se relaciona con birthdate y birthplace (cada autor tiene fecha y lugar de nacimiento)


tags: Guarda las etiquetas para categorizar citas.

Se relaciona con quotes a través de quote_tags (muchas a muchas)


quote_tags: Tabla de unión entre quotes y tags.

Conecta citas con sus etiquetas


birthdate: Almacena fechas de nacimiento.

Usada por la tabla author


birthplace: Guarda lugares de nacimiento.

Usada por la tabla author



Esta estructura permite asociar citas con autores, etiquetar citas, y registrar detalles de los autores de manera organizada y eficiente.