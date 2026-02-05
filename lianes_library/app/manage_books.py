import streamlit as st
from backend import backend_conn
from custom_validation import safe_str, safe_year

st.subheader("Manage Books")

if 'book_message' in st.session_state and st.session_state.book_message:
    st.success(st.session_state.book_message)
    st.session_state.book_message = None

df = backend_conn.get_table("books")

df = df.rename(columns={
    "book_id": "Book ID",
    "ISBN": "ISBN",
    "title": "Title",
    "authors": "Authors",
    "genre": "Genre",
    "publisher": "Publisher",
    "publication_year": "Year",
    "edition": "Edition"
})

exp_table = st.expander("Select a book below to edit or delete", expanded=True)

with exp_table:
    event = st.dataframe(
        df,
        on_select="rerun",
        selection_mode="single-row",
        hide_index=True,
        use_container_width=True
    )

if len(event.selection.rows) > 0:
    selected_row_index = event.selection.rows[0]
    selected_data = df.iloc[selected_row_index]

    col1, col2 = st.columns([3, 1])

    with col1:
        st.write("**Edit Book**")
        with st.form('update_book'):
            title = st.text_input('Title*', value=safe_str(selected_data['Title']))
            authors = st.text_input('Authors', value=safe_str(selected_data['Authors']))
            isbn = st.text_input('ISBN', value=safe_str(selected_data['ISBN']))
            genre = st.text_input('Genre', value=safe_str(selected_data['Genre']))
            publisher = st.text_input('Publisher', value=safe_str(selected_data['Publisher']))
            year = st.number_input('Publication Year', min_value=1800, max_value=2100,
                                   value=safe_year(selected_data['Year']), step=1, placeholder="Leave empty if unknown")
            edition = st.text_input('Edition', value=safe_str(selected_data['Edition']))

            submit = st.form_submit_button('Update Book')

        if submit:
            if not title:
                st.error("Title is required!")
            elif backend_conn.book_exists(title, authors, isbn, genre, publisher, year, edition, exclude_book_id=selected_data['Book ID']):
                st.error("Another book with identical details already exists!")
            else:
                backend_conn.update_book(
                    selected_data['Book ID'], title, authors, isbn, genre, publisher, year, edition
                )
                st.session_state.book_message = f"Book '{title}' updated successfully!"
                st.toast(f"Book '{title}' updated!", icon="✅")
                st.rerun()

    with col2:
        st.write("**Delete Book**")
        st.warning(f"Delete '{selected_data['Title']}'?")
        if st.button("Delete", type="primary"):
            try:
                book_title = selected_data['Title']
                backend_conn.delete_record("books", "book_id", selected_data['Book ID'])
                st.session_state.book_message = f"Book '{book_title}' deleted!"
                st.toast(f"Book '{book_title}' deleted!", icon="🗑️")
                st.rerun()
            except Exception as e:
                st.error(f"Cannot delete: {e}")
