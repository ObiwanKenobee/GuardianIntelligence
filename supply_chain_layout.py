import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from supply_chain_data import (
    generate_supplier_data, generate_risk_metrics,
    generate_supply_chain_events, predict_risk_trends
)

def render_supply_chain_dashboard():
    st.header("Supply Chain Risk Management Dashboard")
    
    # Generate data
    supplier_data = generate_supplier_data()
    risk_metrics = generate_risk_metrics()
    events_data = generate_supply_chain_events()
    risk_predictions = predict_risk_trends(risk_metrics)
    
    # Top KPIs
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Supplier Risk Score", 
                 f"{supplier_data['risk_score'].mean():.1f}",
                 "-0.8")
    with col2:
        st.metric("Average Performance Score", 
                 f"{supplier_data['performance_score'].mean():.1f}",
                 "1.2")
    with col3:
        st.metric("Active Suppliers", 
                 len(supplier_data),
                 "0")
    
    # Risk Map
    st.subheader("Supplier Risk Map")
    fig_risk_map = px.scatter(supplier_data,
                             x='performance_score',
                             y='risk_score',
                             size='delivery_time',
                             color='quality_score',
                             hover_name='name',
                             title='Supplier Risk vs Performance Matrix')
    fig_risk_map.update_layout(height=500)
    st.plotly_chart(fig_risk_map, use_container_width=True)
    
    # Risk Trends with Predictions
    st.subheader("Risk Trends and Forecasts")
    risk_metrics_long = risk_metrics.melt(
        id_vars=['date'],
        value_vars=['supply_disruption_risk', 'quality_risk', 'cost_risk', 'geopolitical_risk'],
        var_name='risk_type',
        value_name='risk_score'
    )
    
    fig_risks = go.Figure()
    for risk_type in ['supply_disruption_risk', 'quality_risk', 'cost_risk', 'geopolitical_risk']:
        # Historical data
        fig_risks.add_trace(go.Scatter(
            x=risk_metrics['date'],
            y=risk_metrics[risk_type],
            name=f'Historical {risk_type.replace("_", " ").title()}',
            line=dict(width=2)
        ))
        
        # Predictions
        fig_risks.add_trace(go.Scatter(
            x=risk_predictions[risk_type]['date'],
            y=risk_predictions[risk_type][f'predicted_{risk_type}'],
            name=f'Predicted {risk_type.replace("_", " ").title()}',
            line=dict(dash='dash')
        ))
    
    fig_risks.update_layout(
        title='Risk Trends with 30-Day Forecast',
        height=400,
        showlegend=True
    )
    st.plotly_chart(fig_risks, use_container_width=True)
    
    # Supply Chain Events Log
    st.subheader("Recent Supply Chain Events")
    events_df = events_data.sort_values('timestamp', ascending=False)
    
    # Color-code severity
    severity_colors = {
        'Low': 'green',
        'Medium': 'yellow',
        'High': 'orange',
        'Critical': 'red'
    }
    
    for _, event in events_df.head(10).iterrows():
        severity_color = severity_colors.get(event['severity'], 'gray')
        st.markdown(
            f"""
            <div style='padding: 10px; border-left: 5px solid {severity_color}; margin: 5px 0;'>
                <strong>{event['event_type']}</strong> - {event['severity']} <br>
                <small>{event['timestamp'].strftime('%Y-%m-%d %H:%M')}</small>
            </div>
            """,
            unsafe_allow_html=True
        )
