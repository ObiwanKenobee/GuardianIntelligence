import sqlite3
from datetime import datetime
import hashlib
import secrets
import streamlit as st

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