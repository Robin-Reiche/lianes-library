import streamlit as st
from backend import backend_conn

st.subheader("Current Customers")

df = backend_conn.get_table("customers")

df = df.rename(columns={
    "customer_id": "Customer ID",
    "email": "Email",
    "first_name": "First Name",
    "last_name": "Last Name",
    "notes": "Notes",
    "max_loans": "Max Loans"
})

st.dataframe(df, use_container_width=True, hide_index=True)
