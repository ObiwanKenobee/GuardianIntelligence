import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from iot_data import (
    generate_sensor_data,
    predict_maintenance_needs,
    calculate_health_scores
)

def render_iot_dashboard():
    st.header("IoT Monitoring & Predictive Maintenance Dashboard")
    
    # Generate sample data
    readings_df, sensors_df = generate_sensor_data()
    health_scores = calculate_health_scores(readings_df)
    maintenance_predictions = predict_maintenance_needs(readings_df)
    
    # Equipment Health Overview
    st.subheader("Equipment Health Status")
    health_cols = st.columns(len(health_scores))
    for idx, (equipment_id, score) in enumerate(health_scores.items()):
        with health_cols[idx]:
            st.metric(
                equipment_id,
                f"{score:.1f}%",
                delta=f"{random.uniform(-2, 2):.1f}%"
            )
    
    # Real-time Monitoring
    st.subheader("Real-time Sensor Readings")
    selected_equipment = st.selectbox(
        "Select Equipment",
        options=readings_df['equipment_id'].unique()
    )
    
    # Filter data for selected equipment
    equipment_data = readings_df[readings_df['equipment_id'] == selected_equipment].copy()
    equipment_data['timestamp'] = pd.to_datetime(equipment_data['timestamp'])
    
    # Create multi-metric visualization
    fig = go.Figure()
    
    # Temperature trend
    fig.add_trace(go.Scatter(
        x=equipment_data['timestamp'],
        y=equipment_data['temperature'],
        name='Temperature (°C)',
        line=dict(color='red')
    ))
    
    # Vibration trend
    fig.add_trace(go.Scatter(
        x=equipment_data['timestamp'],
        y=equipment_data['vibration'],
        name='Vibration',
        line=dict(color='blue'),
        yaxis='y2'
    ))
    
    # Pressure trend
    fig.add_trace(go.Scatter(
        x=equipment_data['timestamp'],
        y=equipment_data['pressure'],
        name='Pressure',
        line=dict(color='green'),
        yaxis='y3'
    ))
    
    # Update layout for multiple y-axes
    fig.update_layout(
        title=f'Sensor Readings for {selected_equipment}',
        yaxis=dict(title='Temperature (°C)', titlefont=dict(color='red')),
        yaxis2=dict(
            title='Vibration',
            titlefont=dict(color='blue'),
            overlaying='y',
            side='right'
        ),
        yaxis3=dict(
            title='Pressure',
            titlefont=dict(color='green'),
            overlaying='y',
            side='right',
            position=0.85
        ),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Maintenance Alerts
    st.subheader("Maintenance Alerts")
    if maintenance_predictions:
        for pred in maintenance_predictions:
            if pred['equipment_id'] == selected_equipment:
                alert_color = 'red' if pred['severity'] == 'High' else 'orange'
                st.markdown(f"""
                    <div style='padding: 20px; border-left: 5px solid {alert_color}; background-color: rgba(255,0,0,0.1)'>
                        <h4 style='color: {alert_color}'>⚠️ {pred['severity']} Priority Alert</h4>
                        <p>{pred['description']}</p>
                        <small>Equipment: {pred['equipment_id']}</small>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.success("No maintenance alerts for selected equipment")
    
    # Equipment Details
    with st.expander("Equipment Details"):
        st.json({
            'Equipment ID': selected_equipment,
            'Location': sensors_df[sensors_df['equipment_id'] == selected_equipment]['location'].iloc[0],
            'Health Score': f"{health_scores[selected_equipment]:.1f}%",
            'Last Maintenance': (datetime.now() - timedelta(days=random.randint(5, 30))).strftime('%Y-%m-%d'),
            'Sensor ID': sensors_df[sensors_df['equipment_id'] == selected_equipment]['sensor_id'].iloc[0]
        })
