import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_generator import (
    generate_manufacturing_data, generate_healthcare_data,
    get_manufacturing_predictions, get_healthcare_predictions
)

def render_manufacturing_dashboard():
    st.header("Manufacturing Industry Dashboard")

    # Get historical data and predictions
    df = generate_manufacturing_data()
    predictions = get_manufacturing_predictions()

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

    # Production Output with Predictions
    fig_production = go.Figure()
    fig_production.add_trace(go.Scatter(
        x=df['date'], y=df['production_output'],
        name='Historical Production',
        line=dict(color='blue')
    ))
    fig_production.add_trace(go.Scatter(
        x=predictions['production_output']['date'],
        y=predictions['production_output']['predicted_production_output'],
        name='Predicted Production',
        line=dict(color='red', dash='dash')
    ))
    fig_production.update_layout(title='Production Output Trend with 30-Day Forecast')
    st.plotly_chart(fig_production, use_container_width=True)

    # Machine Efficiency and Quality Rate Predictions
    col1, col2 = st.columns(2)
    with col1:
        fig_efficiency = go.Figure()
        fig_efficiency.add_trace(go.Scatter(
            x=df['date'], y=df['machine_efficiency'],
            name='Historical Efficiency'
        ))
        fig_efficiency.add_trace(go.Scatter(
            x=predictions['machine_efficiency']['date'],
            y=predictions['machine_efficiency']['predicted_machine_efficiency'],
            name='Predicted Efficiency',
            line=dict(dash='dash')
        ))
        fig_efficiency.update_layout(title='Machine Efficiency Forecast')
        st.plotly_chart(fig_efficiency, use_container_width=True)

    with col2:
        fig_quality = go.Figure()
        fig_quality.add_trace(go.Scatter(
            x=df['date'], y=df['quality_rate'],
            name='Historical Quality'
        ))
        fig_quality.add_trace(go.Scatter(
            x=predictions['quality_rate']['date'],
            y=predictions['quality_rate']['predicted_quality_rate'],
            name='Predicted Quality',
            line=dict(dash='dash')
        ))
        fig_quality.update_layout(title='Quality Rate Forecast')
        st.plotly_chart(fig_quality, use_container_width=True)

def render_healthcare_dashboard():
    st.header("Healthcare Industry Dashboard")

    # Get historical data and predictions
    df = generate_healthcare_data()
    predictions = get_healthcare_predictions()

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

    # Patient Satisfaction with Predictions
    fig_satisfaction = go.Figure()
    fig_satisfaction.add_trace(go.Scatter(
        x=df['date'], y=df['patient_satisfaction'],
        name='Historical Satisfaction',
        line=dict(color='blue')
    ))
    fig_satisfaction.add_trace(go.Scatter(
        x=predictions['patient_satisfaction']['date'],
        y=predictions['patient_satisfaction']['predicted_patient_satisfaction'],
        name='Predicted Satisfaction',
        line=dict(color='red', dash='dash')
    ))
    fig_satisfaction.update_layout(title='Patient Satisfaction Trend with 30-Day Forecast')
    st.plotly_chart(fig_satisfaction, use_container_width=True)

    # Bed Occupancy and Wait Time Predictions
    col1, col2 = st.columns(2)
    with col1:
        fig_occupancy = go.Figure()
        fig_occupancy.add_trace(go.Scatter(
            x=df['date'], y=df['bed_occupancy'],
            name='Historical Occupancy'
        ))
        fig_occupancy.add_trace(go.Scatter(
            x=predictions['bed_occupancy']['date'],
            y=predictions['bed_occupancy']['predicted_bed_occupancy'],
            name='Predicted Occupancy',
            line=dict(dash='dash')
        ))
        fig_occupancy.update_layout(title='Bed Occupancy Forecast')
        st.plotly_chart(fig_occupancy, use_container_width=True)

    with col2:
        fig_wait = go.Figure()
        fig_wait.add_trace(go.Scatter(
            x=df['date'], y=df['average_wait_time'],
            name='Historical Wait Time'
        ))
        fig_wait.add_trace(go.Scatter(
            x=predictions['average_wait_time']['date'],
            y=predictions['average_wait_time']['predicted_average_wait_time'],
            name='Predicted Wait Time',
            line=dict(dash='dash')
        ))
        fig_wait.update_layout(title='Wait Time Forecast')
        st.plotly_chart(fig_wait, use_container_width=True)