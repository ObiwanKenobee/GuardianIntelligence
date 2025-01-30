import streamlit as st

def initialize_session_state():
    if 'current_industry' not in st.session_state:
        st.session_state.current_industry = 'Manufacturing'
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'Dashboard'

def render_sidebar():
    with st.sidebar:
        st.title('Guardian-IO')
        st.subheader('Navigation')

        # Industry Selection
        industry = st.radio(
            "Select Industry",
            ['Manufacturing', 'Healthcare'],
            key='current_industry'
        )

        # View Selection
        view = st.radio(
            "Select View",
            ['Dashboard', 'Supply Chain'],
            key='current_view'
        )

        st.markdown("---")

        # Features Section
        st.subheader("Features")
        st.markdown("""
        - AI Predictive Analytics
        - Supply Chain Risk Mapping
        - IoT Integration
        - Blockchain Traceability
        - ESG Compliance Tracking
        """)

        st.markdown("---")
        st.markdown("v1.1.0 - Guardian-IO Dashboard")