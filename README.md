# Liane's Library Management System

A full-stack library management application built with Python, Streamlit, and MySQL. Designed to help a book lover track her personal lending library - who borrowed what, when it's due, and what's available.

## Project Overview

Liane has a growing book collection and frequently lends books to friends, but struggles to keep track of who has what. This app solves that problem with a simple, intuitive web interface backed by a relational database.

## Features

- **Inventory Management**: View all books, filter by availability, add/edit/delete books
- **Loan Tracking**: Issue loans with configurable duration, track expected return dates
- **Book Returns**: Select and process single or bulk returns
- **Friend Management**: Add/edit/delete borrowers with configurable loan limits
- **Loan History**: View complete lending history
- **Validation**: Duplicate book detection, loan limit enforcement, required field checks

## Tech Stack

- **Frontend**: Streamlit (multi-page app with navigation)
- **Backend**: Python with SQLAlchemy ORM
- **Database**: MySQL with normalized schema (3NF)
- **Security**: Role-based access levels (admin, staff, app), parameterized queries

## Project Structure

```
lianes-library/
├── lianes_library/
│   ├── app/
│   │   ├── app.py                         # Main Streamlit app entry point
│   │   ├── backend.py                     # Database connection (cached)
│   │   ├── library.py                     # Backend class (CRUD operations)
│   │   ├── view_inventory.py              # Book inventory page
│   │   ├── add_book.py                    # Add new book page
│   │   ├── manage_books.py                # Edit/delete books page
│   │   ├── issue_loan.py                  # Loan checkout page
│   │   ├── return_book.py                 # Process returns page
│   │   ├── loan_history.py                # Loan history page
│   │   ├── check_loans.py                 # Loan limit validation
│   │   ├── show_customers.py              # View borrowers page
│   │   ├── create_customer.py             # Add borrower page
│   │   ├── update_customers.py            # Edit/delete borrowers page
│   │   └── custom_validation.py           # Input validation helpers
│   ├── db/
│   │   ├── LianesLibrary_create_schema_script_v2.sql  # Database schema (DDL)
│   │   ├── LianesLibrary_dummy_insert_v2.sql          # Sample data
│   │   └── db_access_levels.sql                       # User roles & permissions
│   └── .env.example                       # Environment variable template
├── requirements.txt
├── .gitignore
└── README.md
```

## Database Schema

```
books (book_id PK, ISBN, title, authors, genre, publisher, publication_year, edition)
  │
  └──< loans (loan_id PK, book_id FK, customer_id FK, loan_date, expected_return_date, return_date, reminder_sent, notes)
  │
customers (customer_id PK, first_name, last_name, email UNIQUE, notes, max_loans)
```

## Setup

### 1. Database

```sql
-- Run the schema script in MySQL
source db/LianesLibrary_create_schema_script_v2.sql;

-- Create access roles
source db/db_access_levels.sql;

-- (Optional) Load sample data
source db/LianesLibrary_dummy_insert_v2.sql;
```

### 2. Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Configure database credentials
cp lianes_library/.env.example lianes_library/.env
# Edit .env with your MySQL credentials
```

### 3. Run

```bash
cd lianes_library/app
streamlit run app.py
```

## Author

Robin Reiche - Data Science Portfolio Project

## License

This project is for educational and portfolio purposes.
