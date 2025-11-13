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
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_accepted BOOLEAN NOT NULL DEFAULT FALSE
);
