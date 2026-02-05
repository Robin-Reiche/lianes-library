import streamlit as st
from backend import backend_conn
import custom_validation as cv
from custom_validation import safe_str

st.subheader("Manage Customers")

if 'customer_message' in st.session_state and st.session_state.customer_message:
    st.success(st.session_state.customer_message)
    st.session_state.customer_message = None

df = backend_conn.get_table("customers")

df = df.rename(columns={
    "customer_id": "Customer ID",
    "email": "Email",
    "first_name": "First Name",
    "last_name": "Last Name",
    "notes": "Notes",
    "max_loans": "Max Loans"
})

exp_table = st.expander("Select a customer below to edit or delete", expanded=True)

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
        st.write("**Edit Customer**")
        with st.form('update_customer'):
            first_name = st.text_input('First Name', value=safe_str(selected_data['First Name']))
            last_name = st.text_input('Last Name', value=safe_str(selected_data['Last Name']))
            email = st.text_input('Email', value=safe_str(selected_data['Email']))
            notes = st.text_input('Notes', value=safe_str(selected_data['Notes']))
            max_loans = st.number_input('Max Loans', value=int(selected_data['Max Loans']), min_value=1)

            submit = st.form_submit_button('Update Customer')

        if submit:
            if ((first_name == selected_data['First Name']) and
                (last_name == selected_data['Last Name']) and
                (email == selected_data['Email']) and
                (notes == selected_data['Notes']) and
                (max_loans == selected_data['Max Loans'])):
                st.warning('No changes detected!')
            else:
                is_email_valid, email_error = cv.validate_email(email)
                is_first_name_valid, first_name_error = cv.validate_field(first_name, "First Name")
                is_last_name_valid, last_name_error = cv.validate_field(last_name, "Last Name")

                errors = [msg for msg in [email_error, first_name_error, last_name_error] if msg]

                if is_email_valid and is_first_name_valid and is_last_name_valid:
                    backend_conn.update_customer(selected_data['Customer ID'], first_name, last_name, email, notes, max_loans)
                    st.session_state.customer_message = f"Customer '{first_name} {last_name}' updated successfully!"
                    st.toast(f"Customer '{first_name} {last_name}' updated!", icon="✅")
                    st.rerun()
                else:
                    st.error("; ".join(errors))

    with col2:
        st.write("**Delete Customer**")
        st.warning(f"Delete '{selected_data['First Name']} {selected_data['Last Name']}'?")
        if st.button("Delete", type="primary"):
            try:
                name = f"{selected_data['First Name']} {selected_data['Last Name']}"
                backend_conn.delete_record("customers", "customer_id", selected_data['Customer ID'])
                st.session_state.customer_message = f"Customer '{name}' deleted!"
                st.toast(f"Customer '{name}' deleted!", icon="🗑️")
                st.rerun()
            except Exception as e:
                st.error(f"Cannot delete: {e}")
