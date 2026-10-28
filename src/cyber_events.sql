-- CSC 4028 - Software Security Testing - Spring 2025
-- Instructor: Thyago Mota
-- Description: The cyber_events database

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    email VARCHAR(30) PRIMARY KEY, 
    name VARCHAR(55) NOT NULL, 
    creation_date DATE NOT NULL, 
    last_active DATE, 
    key VARCHAR(32)
);

DROP TABLE IF EXISTS cyber_events;

CREATE TABLE cyber_events (
    slug VARCHAR(20) PRIMARY KEY,
    event_date DATE NOT NULL, 
    year INT NOT NULL, 
    month INT NOT NULL, 
    actor VARCHAR(75) NOT NULL, 
    actor_type VARCHAR(25) NOT NULL, 
    organization VARCHAR(100) NOT NULL,
    industry_code INT NOT NULL, 
    industry VARCHAR(100) NOT NULL, 
    motive VARCHAR(75) NOT NULL,
    event_type VARCHAR(75) NOT NULL,
    event_subtype VARCHAR(75) NOT NULL, 
    description VARCHAR(300) NOT NULL,
    source_url VARCHAR(200) NOT NULL,
    country VARCHAR(100) NOT NULL,
    actor_country VARCHAR(100) NOT NULL
);
