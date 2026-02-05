import streamlit as st
from backend import backend_conn

st.subheader("Add New Book")

# Show success message from previous submission
if 'book_added' in st.session_state and st.session_state.book_added:
    st.success(st.session_state.book_added)
    st.session_state.book_added = None

with st.form("add_book"):
    title = st.text_input("Title*")
    authors = st.text_input("Authors")
    isbn = st.text_input("ISBN")
    genre = st.text_input("Genre")
    publisher = st.text_input("Publisher")
    publication_year = st.number_input("Publication Year", min_value=1800, max_value=2100, value=None, step=1)
    edition = st.text_input("Edition")
    if st.form_submit_button("Add Book"):
        if not title:
            st.warning("Please enter at least a title.")
        elif backend_conn.book_exists(title, authors, isbn, genre, publisher, publication_year, edition):
            st.error("This book already exists with identical details!")
        else:
            backend_conn.add_book(title, authors, isbn, genre, publisher, publication_year, edition)
            st.session_state.book_added = f"Book '{title}' added successfully!"
            st.toast(f"Book '{title}' added!", icon="✅")
            st.rerun()
