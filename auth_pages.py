import streamlit as st
from models import create_user, verify_user, init_db

def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'industry' not in st.session_state:
        st.session_state.industry = None

def render_login_page():
    st.title('Guardian-IO Login')
    
    with st.form('login_form'):
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        submitted = st.form_submit_button('Login')
        
        if submitted:
            user = verify_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = user['role']
                st.session_state.industry = user['industry']
                st.success('Login successful!')
                st.experimental_rerun()
            else:
                st.error('Invalid username or password')

def render_signup_page():
    st.title('Guardian-IO Signup')
    
    with st.form('signup_form'):
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        role = st.selectbox('Role', ['admin', 'analyst', 'viewer'])
        industry = st.selectbox('Industry', ['Manufacturing', 'Healthcare'])
        submitted = st.form_submit_button('Sign Up')
        
        if submitted:
            if create_user(username, password, role, industry):
                st.success('Account created successfully! Please login.')
            else:
                st.error('Username already exists')

def render_logout_button():
    if st.sidebar.button('Logout'):
        for key in ['authenticated', 'username', 'role', 'industry']:
            st.session_state[key] = None
        st.experimental_rerun()

def check_authentication():
    return st.session_state.authenticated
