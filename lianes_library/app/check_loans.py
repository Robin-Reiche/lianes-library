import streamlit as st
from backend import backend_conn


def allowed_to_borrow(customer_id):
    loans = backend_conn.get_loans_count_and_max_loans(customer_id)
    try:
        max_loans = loans['max_loans'][0]
        count_of_loans = loans['cnt_loan'][0]
    except Exception as e:
        st.write(f"Exception {e}")
    return count_of_loans, max_loans
