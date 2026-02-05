import streamlit as st

st.set_page_config(page_title="Liane's Library Management", layout="wide")

st.title("Liane's Library Management System")

customer_label = 'Friends'

pages = {
    "Books": [
        st.Page("view_inventory.py", title="View Inventory"),
        st.Page("add_book.py", title="Add New Book"),
        st.Page("manage_books.py", title="Edit / Delete Book"),
        st.Page("issue_loan.py", title="Issue Loan"),
        st.Page("return_book.py", title="Return Book"),
        st.Page("loan_history.py", title="View Loan History"),
    ],
    customer_label: [
        st.Page("show_customers.py", title=f"Show Existing {customer_label}"),
        st.Page("create_customer.py", title=f"Add New {customer_label}"),
        st.Page("update_customers.py", title=f"Edit / Delete {customer_label}"),
    ],
}

pg = st.navigation(pages)
pg.run()
