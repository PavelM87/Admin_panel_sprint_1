CREATE EXTENSION pgcrypto;
-- Схема
CREATE SCHEMA IF NOT EXISTS content;

-- Таблицы
CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    certificate TEXT,
    file_path TEXT,
    rating REAL,
    type TEXT NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    film_work_id uuid NOT NULL REFERENCES content.film_work ON DELETE CASCADE,
    genre_id uuid NOT NULL REFERENCES content.genre ON DELETE CASCADE,
    created_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name TEXT NOT NULL,
    birth_date DATE,
    created_at timestamp with time zone,
    updated_at timestamp with time zone  
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    film_work_id uuid NOT NULL REFERENCES content.film_work ON DELETE CASCADE,
    person_id uuid NOT NULL REFERENCES content.person ON DELETE CASCADE,
    role TEXT NOT NULL,
    created_at timestamp with time zone
); 

-- Индексы

CREATE UNIQUE INDEX film_work_genre 
ON content.genre_film_work (
    film_work_id, 
    genre_id
);

CREATE UNIQUE INDEX film_work_person_role 
ON content.person_film_work (
    film_work_id, 
    person_id, 
    role
);
