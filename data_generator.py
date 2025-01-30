import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def generate_manufacturing_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')

    # Generate more realistic time series data with trends and seasonality
    t = np.arange(len(dates))
    trend = 0.1 * t
    seasonality = 50 * np.sin(2 * np.pi * t / 365)

    data = {
        'date': dates,
        'production_output': 1000 + trend + seasonality + np.random.normal(0, 25, len(dates)),
        'machine_efficiency': 92 + 3 * np.sin(2 * np.pi * t / 365) + np.random.normal(0, 1, len(dates)),
        'quality_rate': 97 + np.random.uniform(-1, 1, len(dates)),
        'energy_consumption': 5000 + 200 * np.sin(2 * np.pi * t / 365) + np.random.normal(0, 100, len(dates)),
        'maintenance_incidents': np.random.poisson(2, len(dates))
    }

    return pd.DataFrame(data)

def generate_healthcare_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    t = np.arange(len(dates))
    seasonality = 5 * np.sin(2 * np.pi * t / 365)

    data = {
        'date': dates,
        'patient_satisfaction': 90 + seasonality + np.random.normal(0, 2, len(dates)),
        'bed_occupancy': 80 + 10 * np.sin(2 * np.pi * t / 365) + np.random.normal(0, 5, len(dates)),
        'average_wait_time': 45 + 15 * np.sin(2 * np.pi * t / 365) + np.random.normal(0, 5, len(dates)),
        'staff_availability': 95 + np.random.normal(0, 2, len(dates)),
        'equipment_utilization': 85 + 5 * np.sin(2 * np.pi * t / 365) + np.random.normal(0, 3, len(dates))
    }

    return pd.DataFrame(data)

def predict_metric(df, metric_column, days_to_predict=30):
    """Generate predictions for a given metric using Linear Regression"""
    # Prepare features (days since start)
    X = np.arange(len(df)).reshape(-1, 1)
    y = df[metric_column].values

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Generate future dates and predictions
    future_dates = pd.date_range(
        start=df['date'].iloc[-1] + timedelta(days=1),
        periods=days_to_predict,
        freq='D'
    )

    future_X = np.arange(len(df), len(df) + days_to_predict).reshape(-1, 1)
    predictions = model.predict(future_X)

    return pd.DataFrame({
        'date': future_dates,
        f'predicted_{metric_column}': predictions
    })

def get_manufacturing_predictions():
    """Get predictions for key manufacturing metrics"""
    df = generate_manufacturing_data()
    predictions = {}

    for metric in ['production_output', 'machine_efficiency', 'quality_rate']:
        pred_df = predict_metric(df, metric)
        predictions[metric] = pred_df

    return predictions

def get_healthcare_predictions():
    """Get predictions for key healthcare metrics"""
    df = generate_healthcare_data()
    predictions = {}

    for metric in ['patient_satisfaction', 'bed_occupancy', 'average_wait_time']:
        pred_df = predict_metric(df, metric)
        predictions[metric] = pred_df

    return predictions