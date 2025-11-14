show databases;

-- This will delete the database if it exists, allowing for a clean recreation.
DROP DATABASE IF EXISTS feedback_db;

-- This creates the database but won't cause an error if it already exists.
CREATE DATABASE IF NOT EXISTS feedback_db;

-- This tells MySQL to use the 'feedback_db' for the commands that follow.
USE feedback_db;


-- This creates the table inside 'feedback_db'.
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    movie_title VARCHAR(255),
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


desc feedback;

desc users;

select * from feedback;

select * from users;
