import streamlit as st
from industry_layouts import render_manufacturing_dashboard, render_healthcare_dashboard
from supply_chain_layout import render_supply_chain_dashboard
from utils import initialize_session_state, render_sidebar
from auth_pages import init_session_state, render_login_page, render_signup_page, render_logout_button, check_authentication
from models import init_db, init_supply_chain_tables

# Initialize database
init_db()
init_supply_chain_tables()

# Page configuration
st.set_page_config(
    page_title="Guardian-IO Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session states
init_session_state()
initialize_session_state()

# Authentication check
if not check_authentication():
    tab1, tab2 = st.tabs(['Login', 'Sign Up'])
    with tab1:
        render_login_page()
    with tab2:
        render_signup_page()
else:
    # Render sidebar with logout button
    render_sidebar()
    render_logout_button()

    # Main content based on selected industry and view
    if st.session_state.authenticated:
        if st.session_state.current_view == 'Dashboard':
            if st.session_state.industry == 'Manufacturing':
                render_manufacturing_dashboard()
            elif st.session_state.industry == 'Healthcare':
                render_healthcare_dashboard()
        elif st.session_state.current_view == 'Supply Chain':
            render_supply_chain_dashboard()

        # Footer
        st.markdown("---")
        with st.expander("About Guardian-IO"):
            st.markdown(f"""
            Guardian-IO is an industry-leading platform providing real-time insights and analytics
            across multiple sectors. Our solution integrates advanced technologies including AI,
            blockchain, and IoT to deliver comprehensive business intelligence and operational
            optimization.

            Current User: {st.session_state.username}
            Role: {st.session_state.role}
            Industry: {st.session_state.industry}
            """)