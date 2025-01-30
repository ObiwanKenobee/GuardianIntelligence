import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_generator import (
    generate_manufacturing_data, generate_healthcare_data,
    get_manufacturing_predictions, get_healthcare_predictions
)
import pandas as pd

def render_drill_down_view(data, date, metric):
    """Render detailed drill-down analysis for selected data point"""
    st.subheader(f"Detailed Analysis for {date.strftime('%Y-%m-%d')}")

    # Filter data for selected date
    daily_data = data[data['date'] == date].iloc[0]

    # Display detailed metrics in columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Production Output", f"{daily_data['production_output']:.0f} units")
        st.metric("Energy Consumption", f"{daily_data['energy_consumption']:.0f} kWh")

    with col2:
        st.metric("Quality Rate", f"{daily_data['quality_rate']:.1f}%")
        st.metric("Machine Efficiency", f"{daily_data['machine_efficiency']:.1f}%")

    with col3:
        st.metric("Maintenance Incidents", str(daily_data['maintenance_incidents']))

    # Add trend analysis
    st.subheader("Trend Analysis")

    # Calculate 7-day moving averages
    rolling_data = data.set_index('date').rolling(window=7).mean()

    fig = go.Figure()

    # Add actual values
    fig.add_trace(go.Scatter(
        x=data['date'], 
        y=data[metric],
        name='Actual Values',
        line=dict(color='blue')
    ))

    # Add moving average
    fig.add_trace(go.Scatter(
        x=rolling_data.index,
        y=rolling_data[metric],
        name='7-Day Moving Average',
        line=dict(color='red', dash='dash')
    ))

    fig.update_layout(
        title=f'{metric.replace("_", " ").title()} - 7 Day Trend',
        xaxis_title='Date',
        yaxis_title=metric.replace('_', ' ').title(),
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)

    # Add correlation analysis
    st.subheader("Correlation Analysis")
    correlation_metrics = ['production_output', 'machine_efficiency', 'quality_rate', 'energy_consumption']
    corr_matrix = data[correlation_metrics].corr()

    fig_corr = px.imshow(
        corr_matrix,
        labels=dict(color="Correlation"),
        x=[m.replace('_', ' ').title() for m in correlation_metrics],
        y=[m.replace('_', ' ').title() for m in correlation_metrics]
    )
    fig_corr.update_layout(height=400)
    st.plotly_chart(fig_corr, use_container_width=True)

def render_manufacturing_dashboard():
    st.header("Manufacturing Industry Dashboard")

    # Initialize session state for drill-down
    if 'drill_down_active' not in st.session_state:
        st.session_state.drill_down_active = False
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = None
    if 'selected_metric' not in st.session_state:
        st.session_state.selected_metric = None

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

    # Historical data with click events
    fig_production.add_trace(go.Scatter(
        x=df['date'], 
        y=df['production_output'],
        name='Historical Production',
        line=dict(color='blue'),
        customdata=df[['production_output']],
        hovertemplate='Date: %{x}<br>Output: %{y:.0f} units<extra></extra>'
    ))

    fig_production.add_trace(go.Scatter(
        x=predictions['production_output']['date'],
        y=predictions['production_output']['predicted_production_output'],
        name='Predicted Production',
        line=dict(color='red', dash='dash'),
        hovertemplate='Date: %{x}<br>Predicted Output: %{y:.0f} units<extra></extra>'
    ))

    fig_production.update_layout(
        title='Production Output Trend (Click for Details)',
        height=400,
        hovermode='x unified',
        clickmode='event+select'
    )

    # Handle click events
    clicked = st.plotly_chart(fig_production, use_container_width=True, key='production_chart')
    if clicked is not None and len(clicked['points']) > 0:
        point = clicked['points'][0]
        st.session_state.selected_date = point['x']
        st.session_state.selected_metric = 'production_output'
        st.session_state.drill_down_active = True
        st.experimental_rerun()

    # Render drill-down view if active
    if st.session_state.drill_down_active and st.session_state.selected_date:
        with st.expander("Detailed Analysis", expanded=True):
            render_drill_down_view(df, st.session_state.selected_date, st.session_state.selected_metric)

            if st.button("Close Analysis"):
                st.session_state.drill_down_active = False
                st.session_state.selected_date = None
                st.session_state.selected_metric = None
                st.experimental_rerun()

    # Efficiency and Quality Rate charts with click functionality
    col1, col2 = st.columns(2)

    with col1:
        fig_efficiency = go.Figure()
        fig_efficiency.add_trace(go.Scatter(
            x=df['date'], 
            y=df['machine_efficiency'],
            name='Historical Efficiency',
            customdata=df[['machine_efficiency']],
            hovertemplate='Date: %{x}<br>Efficiency: %{y:.1f}%<extra></extra>'
        ))

        fig_efficiency.add_trace(go.Scatter(
            x=predictions['machine_efficiency']['date'],
            y=predictions['machine_efficiency']['predicted_machine_efficiency'],
            name='Predicted Efficiency',
            line=dict(dash='dash'),
            hovertemplate='Date: %{x}<br>Predicted Efficiency: %{y:.1f}%<extra></extra>'
        ))

        fig_efficiency.update_layout(
            title='Machine Efficiency (Click for Details)',
            height=300,
            hovermode='x unified',
            clickmode='event+select'
        )

        clicked = st.plotly_chart(fig_efficiency, use_container_width=True, key='efficiency_chart')
        if clicked is not None and len(clicked['points']) > 0:
            point = clicked['points'][0]
            st.session_state.selected_date = point['x']
            st.session_state.selected_metric = 'machine_efficiency'
            st.session_state.drill_down_active = True
            st.experimental_rerun()

    with col2:
        fig_quality = go.Figure()
        fig_quality.add_trace(go.Scatter(
            x=df['date'], 
            y=df['quality_rate'],
            name='Historical Quality',
            customdata=df[['quality_rate']],
            hovertemplate='Date: %{x}<br>Quality: %{y:.1f}%<extra></extra>'
        ))

        fig_quality.add_trace(go.Scatter(
            x=predictions['quality_rate']['date'],
            y=predictions['quality_rate']['predicted_quality_rate'],
            name='Predicted Quality',
            line=dict(dash='dash'),
            hovertemplate='Date: %{x}<br>Predicted Quality: %{y:.1f}%<extra></extra>'
        ))

        fig_quality.update_layout(
            title='Quality Rate (Click for Details)',
            height=300,
            hovermode='x unified',
            clickmode='event+select'
        )

        clicked = st.plotly_chart(fig_quality, use_container_width=True, key='quality_chart')
        if clicked is not None and len(clicked['points']) > 0:
            point = clicked['points'][0]
            st.session_state.selected_date = point['x']
            st.session_state.selected_metric = 'quality_rate'
            st.session_state.drill_down_active = True
            st.experimental_rerun()

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