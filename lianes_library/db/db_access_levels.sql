USE LianesLibrary;

-- Create the application user with required permissions
CREATE USER IF NOT EXISTS 'library_app'@'localhost' IDENTIFIED BY '<your_app_password>';

GRANT SELECT ON LianesLibrary.* TO 'library_app'@'localhost';
GRANT INSERT, UPDATE ON LianesLibrary.books TO 'library_app'@'localhost';
GRANT INSERT, UPDATE ON LianesLibrary.customers TO 'library_app'@'localhost';
GRANT INSERT, UPDATE ON LianesLibrary.loans TO 'library_app'@'localhost';
GRANT DELETE ON LianesLibrary.books TO 'library_app'@'localhost';
GRANT DELETE ON LianesLibrary.customers TO 'library_app'@'localhost';
