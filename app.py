import streamlit as st
from login import login
from model import main

## Set page title and layout
st.set_page_config(page_title="Legal Document Analysis", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login()
else:
    main()
