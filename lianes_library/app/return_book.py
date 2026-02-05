import streamlit as st
from backend import backend_conn

st.subheader("Process a Return")

# Show success message from previous action
if 'return_message' in st.session_state and st.session_state.return_message:
    st.success(st.session_state.return_message)
    st.session_state.return_message = None

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
    "expected_return_date": "Expected Return Date",
    "max_loans": "Max Loans"
})

# removing all rows that have a return date set aka aren't on loan anymore
active_loans = final_df[final_df['return_date'].isna()]

# Show active loans
active_loans = active_loans[['Loan ID', 'Book Title', 'Loan Date', 'Expected Return Date', 'First Name', 'Last Name', 'Notes']].sort_values('Loan Date')

if active_loans.empty:
    st.info("No active loans found.")
else:
    event = st.dataframe(
        active_loans,
        on_select="rerun",
        selection_mode="multi-row",
        hide_index=True,
        use_container_width=True
    )

    if len(event.selection.rows) > 0:
        selected_rows = event.selection.rows
        selected_data = active_loans.iloc[selected_rows]

        # get all selected loan IDs
        loan_ids_to_return = selected_data['Loan ID'].tolist()

        # show selected count
        st.info(f"{len(loan_ids_to_return)} book(s) selected for return")

        if st.button("Mark as Returned"):
            for loan_id in loan_ids_to_return:
                backend_conn.update_return_date(loan_id)
            st.session_state.return_message = f"{len(loan_ids_to_return)} loan(s) marked as returned."
            st.toast(f"{len(loan_ids_to_return)} book(s) returned!", icon="✅")
            st.rerun()
