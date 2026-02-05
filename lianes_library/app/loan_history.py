import streamlit as st
from backend import backend_conn

st.subheader("Loan History")

# gather data from all required tables (to be able to display book and lender names)
loans_df = backend_conn.get_table("loans")
customers_df = backend_conn.get_table("customers")
books_df = backend_conn.get_table("books")

# Rename notes columns before merge to avoid confusion
loans_df = loans_df.rename(columns={"notes": "loan_notes"})
customers_df = customers_df.rename(columns={"notes": "customer_notes"})

# merging all tables
final_df = books_df.merge(loans_df, on="book_id")
final_df = final_df.merge(customers_df, on="customer_id")

# renaming columns for table header in display
final_df = final_df.rename(columns={
    "loan_id": "Loan ID",
    "title": "Book Title",
    "authors": "Authors",
    "first_name": "First Name",
    "last_name": "Last Name",
    "loan_notes": "Notes",
    "loan_date": "Loan Date",
    "return_date": "Return Date",
    "expected_return_date": "Expected Return Date"
})

# Filter option
status = st.radio("Show:", ["All Loans", "Returned Only", "Currently On Loan"])

loan_history = final_df[['Loan ID', 'Book Title', 'Loan Date', 'Expected Return Date', 'Return Date', 'First Name', 'Last Name', 'Notes']]

if status == "Returned Only":
    loan_history = loan_history[final_df['Return Date'].notna()]
elif status == "Currently On Loan":
    loan_history = loan_history[final_df['Return Date'].isna()]

loan_history = loan_history.sort_values('Loan Date', ascending=False)

if loan_history.empty:
    st.info("No loans found.")
else:
    st.dataframe(loan_history, use_container_width=True, hide_index=True)
