import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_generator import generate_manufacturing_data, generate_healthcare_data, get_mock_predictions

def render_manufacturing_dashboard():
    st.header("Manufacturing Industry Dashboard")
    
    # Get data
    df = generate_manufacturing_data()
    
    # KPI metrics row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Production Output", 
                 f"{df['production_output'].mean():.0f} units",
                 "2.5%")
    with col2:
        st.metric("Quality Rate", 
                 f"{df['quality_rate'].mean():.1f}%",
                 "0.7%")
    with col3:
        st.metric("Machine Efficiency", 
                 f"{df['machine_efficiency'].mean():.1f}%",
                 "-0.2%")

    # Production Output Trend
    fig_production = px.line(df, x='date', y='production_output',
                           title='Production Output Trend')
    st.plotly_chart(fig_production, use_container_width=True)

    # Machine Efficiency vs Quality Rate
    col1, col2 = st.columns(2)
    with col1:
        fig_scatter = px.scatter(df, x='machine_efficiency', y='quality_rate',
                               title='Efficiency vs Quality Correlation')
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        fig_energy = px.histogram(df, x='energy_consumption',
                                title='Energy Consumption Distribution')
        st.plotly_chart(fig_energy, use_container_width=True)

def render_healthcare_dashboard():
    st.header("Healthcare Industry Dashboard")
    
    # Get data
    df = generate_healthcare_data()
    
    # KPI metrics row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Patient Satisfaction", 
                 f"{df['patient_satisfaction'].mean():.1f}%",
                 "1.2%")
    with col2:
        st.metric("Bed Occupancy", 
                 f"{df['bed_occupancy'].mean():.1f}%",
                 "-0.5%")
    with col3:
        st.metric("Avg Wait Time", 
                 f"{df['average_wait_time'].mean():.0f} min",
                 "-2.3%")

    # Patient Satisfaction Trend
    fig_satisfaction = px.line(df, x='date', y='patient_satisfaction',
                             title='Patient Satisfaction Trend')
    st.plotly_chart(fig_satisfaction, use_container_width=True)

    # Bed Occupancy and Staff Availability
    col1, col2 = st.columns(2)
    with col1:
        fig_occupancy = px.bar(df, x='date', y='bed_occupancy',
                              title='Bed Occupancy Rate')
        st.plotly_chart(fig_occupancy, use_container_width=True)
    
    with col2:
        fig_staff = px.line(df, x='date', y='staff_availability',
                           title='Staff Availability Rate')
        st.plotly_chart(fig_staff, use_container_width=True)
