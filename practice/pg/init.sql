
CREATE DATABASE company_data;

\c company_data;

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    city VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100)
);