import sqlite3
from datetime import datetime
import hashlib
import secrets
import streamlit as st
import numpy as np
from sklearn.ensemble import IsolationForest

def init_db():
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            industry TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, role, industry):
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()
    
    try:
        c.execute(
            'INSERT INTO users (username, password_hash, role, industry) VALUES (?, ?, ?, ?)',
            (username, hash_password(password), role, industry)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()
    
    c.execute('SELECT id, password_hash, role, industry FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if user and user[1] == hash_password(password):
        return {'id': user[0], 'role': user[2], 'industry': user[3]}
    return None

def get_user_role(username):
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()
    
    c.execute('SELECT role FROM users WHERE username = ?', (username,))
    role = c.fetchone()
    conn.close()
    
    return role[0] if role else None


def init_supply_chain_tables():
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()

    # Create suppliers table
    c.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            risk_score FLOAT,
            performance_score FLOAT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create supply_chain_events table
    c.execute('''
        CREATE TABLE IF NOT EXISTS supply_chain_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER,
            event_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
        )
    ''')

    conn.commit()
    conn.close()

def add_supplier(name, location, risk_score, performance_score):
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()

    try:
        c.execute(
            'INSERT INTO suppliers (name, location, risk_score, performance_score) VALUES (?, ?, ?, ?)',
            (name, location, risk_score, performance_score)
        )
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()

def get_suppliers():
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()

    c.execute('SELECT * FROM suppliers')
    suppliers = c.fetchall()
    conn.close()

    return suppliers

def add_supply_chain_event(supplier_id, event_type, severity, description):
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()

    try:
        c.execute(
            'INSERT INTO supply_chain_events (supplier_id, event_type, severity, description) VALUES (?, ?, ?, ?)',
            (supplier_id, event_type, severity, description)
        )
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()

def get_supply_chain_events(days=30):
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()

    c.execute('''
        SELECT e.*, s.name as supplier_name 
        FROM supply_chain_events e 
        JOIN suppliers s ON e.supplier_id = s.id 
        WHERE e.timestamp >= datetime('now', ?) 
        ORDER BY e.timestamp DESC
    ''', (f'-{days} days',))

    events = c.fetchall()
    conn.close()

    return events


def init_iot_tables():
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()

    # Create IoT sensors table
    c.execute('''
        CREATE TABLE IF NOT EXISTS iot_sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT UNIQUE NOT NULL,
            equipment_id TEXT NOT NULL,
            sensor_type TEXT NOT NULL,
            location TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create sensor readings table
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT NOT NULL,
            temperature FLOAT,
            vibration FLOAT,
            pressure FLOAT,
            power_consumption FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sensor_id) REFERENCES iot_sensors (sensor_id)
        )
    ''')

    # Create maintenance_alerts table
    c.execute('''
        CREATE TABLE IF NOT EXISTS maintenance_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT,
            is_resolved BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def register_sensor(sensor_id, equipment_id, sensor_type, location):
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()

    try:
        c.execute(
            'INSERT INTO iot_sensors (sensor_id, equipment_id, sensor_type, location) VALUES (?, ?, ?, ?)',
            (sensor_id, equipment_id, sensor_type, location)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def add_sensor_reading(sensor_id, temperature, vibration, pressure, power_consumption):
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()

    try:
        c.execute(
            'INSERT INTO sensor_readings (sensor_id, temperature, vibration, pressure, power_consumption) VALUES (?, ?, ?, ?, ?)',
            (sensor_id, temperature, vibration, pressure, power_consumption)
        )
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()

def get_sensor_readings(sensor_id, hours=24):
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()

    c.execute('''
        SELECT * FROM sensor_readings 
        WHERE sensor_id = ? AND timestamp >= datetime('now', ?) 
        ORDER BY timestamp DESC
    ''', (sensor_id, f'-{hours} hours'))

    readings = c.fetchall()
    conn.close()

    return readings

def detect_anomalies(sensor_readings, contamination=0.1):
    """
    Detect anomalies in sensor readings using Isolation Forest
    """
    if len(sensor_readings) < 10:  # Need minimum data points
        return []

    # Prepare data for anomaly detection
    X = np.array([[r[2], r[3], r[4], r[5]] for r in sensor_readings])  # temperature, vibration, pressure, power

    # Train isolation forest
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    yhat = iso_forest.fit_predict(X)

    # Return indices of anomalies
    return [i for i, pred in enumerate(yhat) if pred == -1]

def create_maintenance_alert(equipment_id, alert_type, severity, description):
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()

    try:
        c.execute(
            'INSERT INTO maintenance_alerts (equipment_id, alert_type, severity, description) VALUES (?, ?, ?, ?)',
            (equipment_id, alert_type, severity, description)
        )
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()

def get_active_alerts():
    conn = sqlite3.connect('guardian_io.db')
    c = conn.cursor()

    c.execute('''
        SELECT * FROM maintenance_alerts 
        WHERE is_resolved = FALSE 
        ORDER BY created_at DESC
    ''')

    alerts = c.fetchall()
    conn.close()

    return alerts