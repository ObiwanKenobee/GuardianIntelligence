import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
import random

def generate_supplier_data(n_suppliers=10):
    """Generate mock supplier data with risk and performance metrics"""
    locations = ['USA', 'China', 'India', 'Germany', 'Brazil', 'Japan', 'Mexico', 'Vietnam', 'Thailand', 'Malaysia']
    company_types = ['Manufacturing', 'Raw Materials', 'Electronics', 'Logistics', 'Components']
    
    suppliers = []
    for i in range(n_suppliers):
        supplier = {
            'name': f"{random.choice(company_types)} Supplier {i+1}",
            'location': random.choice(locations),
            'risk_score': round(random.uniform(1, 10), 2),
            'performance_score': round(random.uniform(60, 100), 2),
            'delivery_time': round(random.uniform(5, 30)),
            'quality_score': round(random.uniform(80, 100), 2),
            'cost_variance': round(random.uniform(-10, 10), 2)
        }
        suppliers.append(supplier)
    
    return pd.DataFrame(suppliers)

def generate_risk_metrics():
    """Generate risk metrics data for visualization"""
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    t = np.arange(len(dates))
    
    # Generate risk metrics with trends and seasonality
    risk_data = {
        'date': dates,
        'supply_disruption_risk': 5 + 2 * np.sin(2 * np.pi * t / 365) + np.random.normal(0, 0.5, len(dates)),
        'quality_risk': 3 + np.random.normal(0, 0.3, len(dates)),
        'cost_risk': 4 + 1.5 * np.sin(2 * np.pi * t / 180) + np.random.normal(0, 0.4, len(dates)),
        'geopolitical_risk': 6 + np.random.normal(0, 0.2, len(dates))
    }
    
    return pd.DataFrame(risk_data)

def generate_supply_chain_events(n_events=50):
    """Generate mock supply chain events for the event log"""
    event_types = ['Delivery Delay', 'Quality Issue', 'Price Increase', 'Natural Disaster', 'Political Unrest']
    severities = ['Low', 'Medium', 'High', 'Critical']
    
    events = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    for _ in range(n_events):
        event = {
            'timestamp': start_date + timedelta(
                seconds=random.randint(0, int((end_date - start_date).total_seconds()))
            ),
            'event_type': random.choice(event_types),
            'severity': random.choice(severities),
            'supplier_id': random.randint(1, 10)
        }
        events.append(event)
    
    df = pd.DataFrame(events)
    df = df.sort_values('timestamp')
    return df

def predict_risk_trends(risk_data, days_to_predict=30):
    """Generate predictions for risk metrics"""
    predictions = {}
    
    for column in ['supply_disruption_risk', 'quality_risk', 'cost_risk', 'geopolitical_risk']:
        # Prepare data for prediction
        X = np.arange(len(risk_data)).reshape(-1, 1)
        y = risk_data[column].values.reshape(-1, 1)
        
        # Scale the data
        scaler = MinMaxScaler()
        y_scaled = scaler.fit_transform(y)
        
        # Generate future dates
        future_dates = pd.date_range(
            start=risk_data['date'].iloc[-1] + timedelta(days=1),
            periods=days_to_predict,
            freq='D'
        )
        
        # Generate predictions with trend and seasonality
        future_X = np.arange(len(risk_data), len(risk_data) + days_to_predict)
        trend = 0.1 * future_X
        seasonality = 2 * np.sin(2 * np.pi * future_X / 365)
        
        predictions[column] = pd.DataFrame({
            'date': future_dates,
            f'predicted_{column}': trend + seasonality + np.random.normal(0, 0.2, len(future_dates))
        })
    
    return predictions
