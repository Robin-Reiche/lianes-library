DROP SCHEMA IF EXISTS LianesLibrary;
CREATE SCHEMA LianesLibrary;
USE LianesLibrary;

CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    ISBN VARCHAR(255) NULL,
    title VARCHAR(255) NOT NULL,
    authors VARCHAR(255) NULL,
    genre VARCHAR(255) NULL,
    publisher VARCHAR(255) NULL,
    publication_year INT NULL,
    edition VARCHAR(255) NULL
);

CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NULL, -- UNIQUE to prevent duplicate accounts
    notes VARCHAR(255) NULL,
    max_loans INT DEFAULT 2
);

CREATE TABLE loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    customer_id INT NOT NULL,
    loan_date DATE NOT NULL,
    expected_return_date DATE NULL,
    return_date DATE NULL,
    reminder_sent INT DEFAULT 0,
    notes VARCHAR(255) NULL,
    FOREIGN KEY (book_id) REFERENCES books (book_id),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);