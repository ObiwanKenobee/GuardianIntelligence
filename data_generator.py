import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_manufacturing_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    
    data = {
        'date': dates,
        'production_output': np.random.normal(1000, 50, len(dates)),
        'machine_efficiency': np.random.uniform(85, 98, len(dates)),
        'quality_rate': np.random.uniform(95, 99.9, len(dates)),
        'energy_consumption': np.random.normal(5000, 200, len(dates)),
        'maintenance_incidents': np.random.poisson(2, len(dates))
    }
    
    return pd.DataFrame(data)

def generate_healthcare_data():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    
    data = {
        'date': dates,
        'patient_satisfaction': np.random.uniform(85, 98, len(dates)),
        'bed_occupancy': np.random.uniform(70, 95, len(dates)),
        'average_wait_time': np.random.normal(45, 10, len(dates)),
        'staff_availability': np.random.uniform(90, 99, len(dates)),
        'equipment_utilization': np.random.uniform(75, 95, len(dates))
    }
    
    return pd.DataFrame(data)

def get_mock_predictions():
    future_dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    predictions = {
        'date': future_dates,
        'predicted_demand': np.random.normal(1000, 100, len(future_dates))
    }
    return pd.DataFrame(predictions)
