-- Establecer la codificación de caracteres a UTF8
\encoding UTF8

-- Conectarse a la base de datos postgres
\c postgres

-- Cerrar todas las conexiones activas a la base de datos 'quotes'
SELECT pg_terminate_backend(pid)  
FROM pg_stat_activity
WHERE datname = 'quotes' AND pid <> pg_backend_pid();

-- Conectarse a la base de datos 'quotes'
\c quotes

-- Establecer la codificación de cliente a UTF8
SET client_encoding TO 'UTF8';

-- Agregar un comentario descriptivo sobre la base de datos 'quotes'
COMMENT ON DATABASE quotes
    IS 'Base de datos para Scraping Quotes';

-- Crear el esquema si no existe
CREATE SCHEMA IF NOT EXISTS quotes;

-- -----------------------------  Eliminar las tablas si existen  ----------------------------- --
DROP TABLE IF EXISTS quotes.author CASCADE;
DROP TABLE IF EXISTS quotes.quotes CASCADE;
DROP TABLE IF EXISTS quotes.tags CASCADE;
DROP TABLE IF EXISTS quotes.quote_tags CASCADE;
DROP TABLE IF EXISTS quotes.birthdate CASCADE;
DROP TABLE IF EXISTS quotes.birthplace CASCADE;

-- -----------------------------  Crear las tablas  ----------------------------- --

-- Crear la tabla de fechas de nacimiento
CREATE TABLE quotes.birthdate (
    id SERIAL PRIMARY KEY,
    birthdate DATE NOT NULL
);

-- Agregar comentarios a la tabla de fechas de nacimiento
COMMENT ON TABLE quotes.birthdate IS 'Tabla que almacena las fechas de nacimiento';
COMMENT ON COLUMN quotes.birthdate.birthdate IS 'Fecha de nacimiento';

-- Crear la tabla de lugares de nacimiento
CREATE TABLE quotes.birthplace (
    id SERIAL PRIMARY KEY,
    birthplace VARCHAR(255) NOT NULL
);

-- Agregar comentarios a la tabla de lugares de nacimiento
COMMENT ON TABLE quotes.birthplace IS 'Tabla que almacena los lugares de nacimiento';
COMMENT ON COLUMN quotes.birthplace.birthplace IS 'Lugar de nacimiento';

-- Crear la tabla de autores con referencias a las nuevas tablas
CREATE TABLE quotes.author (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthdate_id INTEGER REFERENCES quotes.birthdate(id),
    birthplace_id INTEGER REFERENCES quotes.birthplace(id),
    description TEXT
);

-- Agregar comentarios a la nueva tabla de autores
COMMENT ON TABLE quotes.author IS 'Tabla que almacena información sobre los autores de las citas';
COMMENT ON COLUMN quotes.author.name IS 'Nombre del autor';
COMMENT ON COLUMN quotes.author.birthdate_id IS 'ID de la fecha de nacimiento del autor';
COMMENT ON COLUMN quotes.author.birthplace_id IS 'ID del lugar de nacimiento del autor';
COMMENT ON COLUMN quotes.author.description IS 'Descripción del autor';


-- Crear la tabla de etiquetas
CREATE TABLE quotes.tags (
    id SERIAL PRIMARY KEY,
    tag VARCHAR(50) UNIQUE
);

-- Agregar comentarios a la tabla de etiquetas
COMMENT ON TABLE quotes.tags IS 'Tabla que almacena las etiquetas de las citas';
COMMENT ON COLUMN quotes.tags.tag IS 'Etiqueta asociada a una cita';

-- Crear la tabla de citas
CREATE TABLE quotes.quotes (
    id SERIAL PRIMARY KEY,
    quote TEXT NOT NULL,
    author_id INTEGER REFERENCES quotes.author(id)
);

-- Agregar comentarios a la tabla de citas
COMMENT ON TABLE quotes.quotes IS 'Tabla que almacena las citas';
COMMENT ON COLUMN quotes.quotes.quote IS 'Texto de la cita';
COMMENT ON COLUMN quotes.quotes.author_id IS 'ID del autor de la cita';


-- Crear la tabla de relación entre citas y etiquetas
CREATE TABLE quotes.quote_tags (
    id SERIAL PRIMARY KEY,
    quote_id INTEGER REFERENCES quotes.quotes(id),
    tag_id INTEGER REFERENCES quotes.tags(id)
);

-- Agregar comentarios a la tabla de relación entre citas y etiquetas
COMMENT ON TABLE quotes.quote_tags IS 'Tabla que almacena la relación entre citas y etiquetas';
COMMENT ON COLUMN quotes.quote_tags.quote_id IS 'ID de la cita';
COMMENT ON COLUMN quotes.quote_tags.tag_id IS 'ID de la etiqueta';



-- ------------------------------------------------- Crear la vista con Cita, Autor y Tags

CREATE VIEW quotes.view_quote_details AS
SELECT 
    q.quote AS citation,
    a.name AS author,
    STRING_AGG(t.tag, ', ') AS tags
FROM 
    quotes.quotes q
JOIN 
    quotes.author a ON q.author_id = a.id
LEFT JOIN 
    quotes.quote_tags qt ON q.id = qt.quote_id
LEFT JOIN 
    quotes.tags t ON qt.tag_id = t.id
GROUP BY 
    q.id, q.quote, a.name
ORDER BY 
    q.id ASC;