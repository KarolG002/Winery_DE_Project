--SELECT 'CREATE DATABASE winedb'
--WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'winedb')\gexec

CREATE TABLE IF NOT EXISTS red (
    id SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Country VARCHAR(255) NOT NULL,
    Region VARCHAR(255) NOT NULL,
    Winery VARCHAR(255) NOT NULL,
    Rating DECIMAL(3,1) NOT NULL,
    NumberOfRatings INT NOT NULL,
    Price Numeric NOT NULL,
    Year VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS rose  (
    id SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Country VARCHAR(255) NOT NULL,
    Region VARCHAR(255) NOT NULL,
    Winery VARCHAR(255) NOT NULL,
    Rating DECIMAL(3,1) NOT NULL,
    NumberOfRatings INT NOT NULL,
    Price Numeric NOT NULL,
    Year VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS sparkling  (
    id SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Country VARCHAR(255) NOT NULL,
    Region VARCHAR(255) NOT NULL,
    Winery VARCHAR(255) NOT NULL,
    Rating DECIMAL(3,1) NOT NULL,
    NumberOfRatings INT NOT NULL,
    Price Numeric NOT NULL,
    Year VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS white (
    id SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Country VARCHAR(255) NOT NULL,
    Region VARCHAR(255) NOT NULL,
    Winery VARCHAR(255) NOT NULL,
    Rating DECIMAL(3,1) NOT NULL,
    NumberOfRatings INT NOT NULL,
    Price Numeric NOT NULL,
    Year VARCHAR(255) NOT NULL
);