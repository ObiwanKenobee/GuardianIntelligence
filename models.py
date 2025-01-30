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
