import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_sensor_data(num_sensors=5, hours=24):
    """Generate mock IoT sensor data"""
    equipment_types = ['Pump', 'Motor', 'Compressor', 'Conveyor', 'Robot']
    locations = ['Assembly Line A', 'Assembly Line B', 'Packaging', 'Warehouse', 'Quality Control']

    # Generate base sensor data
    sensors = []
    for i in range(num_sensors):
        sensor = {
            'sensor_id': f'SENSOR_{i+1}',
            'equipment_id': f'{random.choice(equipment_types)}_{i+1}',
            'sensor_type': 'Multi-Metric',
            'location': random.choice(locations)
        }
        sensors.append(sensor)

    # Generate time series data for each sensor
    timestamps = pd.date_range(
        end=datetime.now(),
        periods=hours * 60,  # One reading per minute
        freq='1min'
    )

    all_readings = []
    for sensor in sensors:
        # Generate normal operating parameters with some random variation
        base_temp = random.uniform(50, 70)
        base_vibration = random.uniform(0.1, 0.3)
        base_pressure = random.uniform(90, 110)
        base_power = random.uniform(0.8, 1.2)

        # Add some trends and patterns
        t = np.arange(len(timestamps))
        temp_trend = 0.1 * np.sin(2 * np.pi * t / (60 * 12))  # 12-hour cycle
        vibr_trend = 0.05 * np.sin(2 * np.pi * t / (60 * 4))  # 4-hour cycle

        # Generate readings with trends and random noise
        for timestamp in timestamps:
            idx = len(all_readings)
            reading = {
                'sensor_id': sensor['sensor_id'],
                'equipment_id': sensor['equipment_id'],
                'timestamp': timestamp,
                'temperature': base_temp + temp_trend[idx % len(temp_trend)] + np.random.normal(0, 0.5),
                'vibration': base_vibration + vibr_trend[idx % len(vibr_trend)] + np.random.normal(0, 0.02),
                'pressure': base_pressure + np.random.normal(0, 1.0),
                'power_consumption': base_power + np.random.normal(0, 0.05)
            }

            # Introduce anomalies occasionally (1% chance)
            if random.random() < 0.01:
                reading['temperature'] *= 1.5  # Sudden temperature spike
                reading['vibration'] *= 2.0    # Increased vibration

            all_readings.append(reading)

    return pd.DataFrame(all_readings), pd.DataFrame(sensors)

def predict_maintenance_needs(readings_df, threshold_multiplier=1.5):
    """Predict maintenance needs based on sensor readings"""
    predictions = []

    for equipment_id in readings_df['equipment_id'].unique():
        equipment_data = readings_df[readings_df['equipment_id'] == equipment_id]

        # Calculate baseline statistics
        temp_mean = equipment_data['temperature'].mean()
        temp_std = equipment_data['temperature'].std()
        vibr_mean = equipment_data['vibration'].mean()
        vibr_std = equipment_data['vibration'].std()

        # Check for concerning patterns
        high_temp = equipment_data['temperature'] > (temp_mean + threshold_multiplier * temp_std)
        high_vibration = equipment_data['vibration'] > (vibr_mean + threshold_multiplier * vibr_std)

        if high_temp.any() or high_vibration.any():
            severity = 'High' if (high_temp & high_vibration).any() else 'Medium'
            prediction = {
                'equipment_id': equipment_id,
                'alert_type': 'Predictive Maintenance',
                'severity': severity,
                'description': (
                    f"Abnormal patterns detected: "
                    f"Temperature: {'Yes' if high_temp.any() else 'No'}, "
                    f"Vibration: {'Yes' if high_vibration.any() else 'No'}"
                )
            }
            predictions.append(prediction)

    return predictions

def calculate_health_scores(readings_df):
    """Calculate equipment health scores based on sensor readings"""
    health_scores = {}

    for equipment_id in readings_df['equipment_id'].unique():
        equipment_data = readings_df[readings_df['equipment_id'] == equipment_id]

        # Calculate normalized metrics
        temp_score = 100 - (equipment_data['temperature'].std() / equipment_data['temperature'].mean() * 100)
        vibr_score = 100 - (equipment_data['vibration'].std() / equipment_data['vibration'].mean() * 100)
        pressure_score = 100 - (equipment_data['pressure'].std() / equipment_data['pressure'].mean() * 100)
        power_score = 100 - (equipment_data['power_consumption'].std() / equipment_data['power_consumption'].mean() * 100)

        # Calculate overall health score (weighted average)
        health_score = (
            0.3 * temp_score +
            0.3 * vibr_score +
            0.2 * pressure_score +
            0.2 * power_score
        )

        health_scores[equipment_id] = min(max(health_score, 0), 100)  # Clamp between 0 and 100

    return health_scores