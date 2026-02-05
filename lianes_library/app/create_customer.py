import streamlit as st
from backend import backend_conn

st.subheader("Create New Customer")

# Show success message from previous submission
if 'customer_created' in st.session_state and st.session_state.customer_created:
    st.success(st.session_state.customer_created)
    st.session_state.customer_created = None

with st.form("create_customer"):
    first_name = st.text_input("First Name*")
    last_name = st.text_input("Last Name*")
    email = st.text_input("Email")
    notes = st.text_input("Notes")
    max_loans = st.number_input("Max loans", min_value=1, value=1)

    if st.form_submit_button("Create Customer"):
        if not first_name or not last_name:
            st.warning("First Name and Last Name are required!")
        else:
            try:
                backend_conn.create_customer(first_name, last_name, email, notes, max_loans)
                st.session_state.customer_created = f"Customer '{first_name} {last_name}' created successfully!"
                st.toast(f"Customer '{first_name} {last_name}' created!", icon="✅")
                st.rerun()
            except Exception as e:
                if "Duplicate entry" in str(e) and "email" in str(e):
                    st.error(f"A customer with email '{email}' already exists!")
                else:
                    st.error(f"Error creating customer: {e}")
