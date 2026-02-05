import streamlit as st
from library import LianesLibraryApp

# Initialize the backend (credentials loaded from .env)
@st.cache_resource
def get_backend():
    return LianesLibraryApp()

backend_conn = get_backend()