USE LianesLibrary;

CREATE USER IF NOT EXISTS 'librarian_admin'@'localhost' IDENTIFIED BY '<your_admin_password>';
GRANT ALL PRIVILEGES ON LianesLibrary.* TO 'librarian_admin'@'localhost';

CREATE USER IF NOT EXISTS 'library_staff'@'localhost' IDENTIFIED BY '<your_staff_password>';

-- Staff can view and edit records, but can't "Delete" the inventory or users
GRANT SELECT, INSERT, UPDATE ON LianesLibrary.books TO 'library_staff'@'localhost';
GRANT SELECT, INSERT, UPDATE ON LianesLibrary.customers TO 'library_staff'@'localhost';
GRANT SELECT, INSERT, UPDATE ON LianesLibrary.loans TO 'library_staff'@'localhost';

CREATE USER IF NOT EXISTS 'library_app'@'localhost' IDENTIFIED BY '<your_app_password>';

-- App needs to read everything and manage books, customers, and loans
GRANT SELECT ON LianesLibrary.* TO 'library_app'@'localhost';
GRANT INSERT ON LianesLibrary.loans TO 'library_app'@'localhost';
GRANT UPDATE ON LianesLibrary.loans TO 'library_app'@'localhost';
GRANT INSERT, UPDATE ON LianesLibrary.customers TO 'library_app'@'localhost';
GRANT INSERT, UPDATE ON LianesLibrary.books TO 'library_app'@'localhost';

SHOW GRANTS FOR 'library_staff'@'localhost';
SHOW GRANTS FOR 'library_app'@'localhost';

GRANT DELETE ON LianesLibrary.customers TO 'library_app'@'localhost';
GRANT DELETE ON LianesLibrary.books TO 'library_app'@'localhost';

ALTER TABLE loans ADD COLUMN notes VARCHAR(255) NULL;
