import streamlit as st
import check_loans
from backend import backend_conn
from datetime import date, timedelta

st.subheader("Checkout a Book")

if 'loan_message' in st.session_state and st.session_state.loan_message:
    st.success(st.session_state.loan_message)
    st.session_state.loan_message = None

col1, col2 = st.columns(2)
with col1:
    available_books = backend_conn.get_available_books()
    available_books = available_books.sort_values('title', ascending=True)
    book_options = {row['title']: row['book_id'] for _, row in available_books.iterrows()}
    selected_book = st.selectbox("Select Book", options=list(book_options.keys()))

with col2:
    customers = backend_conn.get_list_of_available_customers()
    customer_options = {f"{row['first_name']} {row['last_name']}": row['customer_id'] for _, row in customers.iterrows()}
    selected_customer = st.selectbox("Select Friend", options=list(customer_options.keys()))

col3, col4 = st.columns(2)
with col3:
    loan_days = st.number_input("Loan Duration (days)", min_value=1, max_value=365, value=14)

with col4:
    expected_return = date.today() + timedelta(days=loan_days)
    st.text_input("Expected Return Date", value=expected_return.strftime("%Y-%m-%d"), disabled=True)

notes = st.text_input("Notes (optional)")

if st.button("Confirm Loan"):
    current_loans, max_loans = check_loans.allowed_to_borrow(customer_options[selected_customer])
    if max_loans <= current_loans:
        st.error(f"Current unreturned loans of {current_loans} have reached the maximum allowed of {max_loans}")
    else:
        try:
            backend_conn.add_loan(book_options[selected_book], customer_options[selected_customer], days=loan_days, notes=notes if notes else None)
            st.session_state.loan_message = f"Successfully issued '{selected_book}' to {selected_customer}! Return by {expected_return.strftime('%Y-%m-%d')}"
            st.toast("Book issued!", icon="✅")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
