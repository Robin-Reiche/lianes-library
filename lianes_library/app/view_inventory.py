import streamlit as st
from backend import backend_conn

st.subheader("Current Inventory")

# Get book counts
all_books = backend_conn.get_table("books")
available_books = backend_conn.get_available_books()
total_count = len(all_books)
available_count = len(available_books)
on_loan_count = total_count - available_count

# Display metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Books", total_count)
col2.metric("Available", available_count)
col3.metric("On Loan", on_loan_count)

status = st.radio("Show:", ["All Books", "Available Only"])
if status == "Available Only":
    df = available_books
else:
    df = all_books

st.dataframe(df, use_container_width=True, hide_index = True)
