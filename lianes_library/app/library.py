import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()


class LianesLibraryApp:
    def __init__(self, username=None, password=None, host=None, db=None):
        user = username or os.getenv('DB_USER', 'library_app')
        pw = password or os.getenv('DB_PASSWORD', '')
        host = host or os.getenv('DB_HOST', 'localhost')
        db = db or os.getenv('DB_NAME', 'LianesLibrary')
        self.url = f"mysql+pymysql://{user}:{pw}@{host}/{db}"
        self.engine = create_engine(self.url)

    def _execute_query(self, query, params=None):
        """Execute a non-returning query (INSERT/UPDATE/DELETE)."""
        with self.engine.begin() as conn:
            conn.execute(text(query), params or {})

    # --- READ ---
    def get_table(self, table_name):
        return pd.read_sql(f"SELECT * FROM {table_name}", con=self.engine)

    def get_available_books(self):
        """Return books that are not currently on loan."""
        query = """
            SELECT b.* FROM books b
            LEFT JOIN loans l ON b.book_id = l.book_id AND l.return_date IS NULL
            WHERE l.loan_id IS NULL
            """
        return pd.read_sql(query, con=self.engine)

    def get_loans_count_and_max_loans(self, customer_id):
        query = """
            SELECT c.customer_id, c.max_loans, COUNT(l.loan_id) cnt_loan
            FROM customers c
            LEFT JOIN loans l ON c.customer_id = l.customer_id AND l.return_date IS NULL
            WHERE c.customer_id = :customer_id
            GROUP BY c.customer_id
            """
        return pd.read_sql(text(query), con=self.engine, params={"customer_id": customer_id})

    def get_list_of_available_customers(self):
        """Return customers who haven't reached their loan limit."""
        query = """
            SELECT c.customer_id, c.first_name, c.last_name, c.email, c.notes, c.max_loans
            FROM customers c
            LEFT JOIN loans l ON c.customer_id = l.customer_id AND l.return_date IS NULL
            GROUP BY c.customer_id
            HAVING max_loans > COUNT(l.loan_id)
            """
        return pd.read_sql(text(query), con=self.engine)

    def book_exists(self, title, authors, isbn, genre, publisher, publication_year, edition, exclude_book_id=None):
        """Check if a book with identical details already exists."""
        query = """
            SELECT COUNT(*) as cnt FROM books
            WHERE (title = :title OR (title IS NULL AND :title IS NULL))
            AND (authors = :authors OR (authors IS NULL AND :authors IS NULL))
            AND (ISBN = :isbn OR (ISBN IS NULL AND :isbn IS NULL))
            AND (genre = :genre OR (genre IS NULL AND :genre IS NULL))
            AND (publisher = :publisher OR (publisher IS NULL AND :publisher IS NULL))
            AND (publication_year = :pub_year OR (publication_year IS NULL AND :pub_year IS NULL))
            AND (edition = :edition OR (edition IS NULL AND :edition IS NULL))
            """
        params = {
            "title": title or None, "authors": authors or None, "isbn": isbn or None,
            "genre": genre or None, "publisher": publisher or None,
            "pub_year": publication_year or None, "edition": edition or None
        }
        if exclude_book_id:
            query += " AND book_id != :book_id"
            params["book_id"] = exclude_book_id
        result = pd.read_sql(text(query), con=self.engine, params=params)
        return result['cnt'].iloc[0] > 0

    # --- CREATE ---
    def add_loan(self, book_id, customer_id, days=14, notes=None):
        query = """
            INSERT INTO loans (book_id, customer_id, loan_date, expected_return_date, notes)
            VALUES (:book_id, :customer_id, CURDATE(), DATE_ADD(CURDATE(), INTERVAL :days DAY), :notes)
            """
        self._execute_query(query, {
            "book_id": book_id, "customer_id": customer_id, "days": days, "notes": notes
        })

    def create_customer(self, first_name, last_name, email, notes, max_loans):
        query = """
            INSERT INTO customers (first_name, last_name, email, notes, max_loans)
            VALUES (:first_name, :last_name, :email, :notes, :max_loans)
            """
        self._execute_query(query, {
            "first_name": first_name, "last_name": last_name,
            "email": email, "notes": notes, "max_loans": max_loans
        })

    def add_book(self, title, authors, isbn, genre, publisher, publication_year, edition):
        query = """
            INSERT INTO books (title, authors, ISBN, genre, publisher, publication_year, edition)
            VALUES (:title, :authors, :isbn, :genre, :publisher, :pub_year, :edition)
            """
        self._execute_query(query, {
            "title": title, "authors": authors, "isbn": isbn, "genre": genre,
            "publisher": publisher, "pub_year": publication_year, "edition": edition
        })

    # --- UPDATE ---
    def update_return_date(self, loan_id):
        query = """
            UPDATE loans
            SET return_date = CURDATE()
            WHERE loan_id = :loan_id
            """
        self._execute_query(query, {"loan_id": loan_id})

    def update_customer(self, customer_id, first_name, last_name, email, notes, max_loans):
        query = """
            UPDATE customers
            SET first_name = :first_name, last_name = :last_name, email = :email,
                notes = :notes, max_loans = :max_loans
            WHERE customer_id = :customer_id
            """
        self._execute_query(query, {
            "customer_id": customer_id, "first_name": first_name, "last_name": last_name,
            "email": email, "notes": notes, "max_loans": max_loans
        })

    def update_book(self, book_id, title, authors, isbn, genre, publisher, publication_year, edition):
        query = """
            UPDATE books
            SET title = :title, authors = :authors, ISBN = :isbn, genre = :genre,
                publisher = :publisher, publication_year = :pub_year, edition = :edition
            WHERE book_id = :book_id
            """
        self._execute_query(query, {
            "book_id": book_id, "title": title, "authors": authors, "isbn": isbn,
            "genre": genre, "publisher": publisher, "pub_year": publication_year, "edition": edition
        })

    # --- DELETE ---
    def delete_record(self, table, record_id_name, record_id):
        query = f"DELETE FROM {table} WHERE {record_id_name} = :id"
        self._execute_query(query, {"id": record_id})
