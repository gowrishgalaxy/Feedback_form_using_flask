show databases;

-- This will delete the database if it exists, allowing for a clean recreation.
DROP DATABASE IF EXISTS feedback_db;

-- This creates the database but won't cause an error if it already exists.
CREATE DATABASE IF NOT EXISTS feedback_db;

-- This tells MySQL to use the 'feedback_db' for the commands that follow.
USE feedback_db;

-- This will show that there are no tables in the database yet.
SHOW TABLES;

-- Alternative: If you only want to delete the tables but not the whole database,
-- you can uncomment the following lines.
-- DROP TABLE IF EXISTS feedback;
-- DROP TABLE IF EXISTS users;

-- This creates the table inside 'feedback_db'.
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    movie_title VARCHAR(255),
    rating INT,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_accepted BOOLEAN NOT NULL DEFAULT FALSE
);

-- This creates the 'users' table for authentication and roles.
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert the predefined admin user with a hashed password for 'IMDB123'.
-- The role is 'admin' to match the check in app.py.
INSERT INTO users (username, password, role) VALUES ('IMDB', 'pbkdf2:sha256:600000$sY16i3aLqfLpYqG5$d7a1cffc2e45c3c213b07323b705b7314c6892523a185496b3d85325511e3919', 'admin');


desc feedback;

desc users;

-- This will now list the 'feedback' and 'users' tables.
SHOW TABLES;

select * from feedback;

select * from users;
