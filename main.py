import streamlit as st
from industry_layouts import render_manufacturing_dashboard, render_healthcare_dashboard
from utils import initialize_session_state, render_sidebar

# Page configuration
st.set_page_config(
    page_title="Guardian-IO Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Render sidebar
render_sidebar()

# Main content based on selected industry
if st.session_state.current_industry == 'Manufacturing':
    render_manufacturing_dashboard()
elif st.session_state.current_industry == 'Healthcare':
    render_healthcare_dashboard()

# Footer
st.markdown("---")
with st.expander("About Guardian-IO"):
    st.markdown("""
    Guardian-IO is an industry-leading platform providing real-time insights and analytics
    across multiple sectors. Our solution integrates advanced technologies including AI,
    blockchain, and IoT to deliver comprehensive business intelligence and operational
    optimization.
    """)
