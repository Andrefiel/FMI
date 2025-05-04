import sqlite3
import os
from datetime import datetime

DB_FILE = "monitoring_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_type TEXT,
            path TEXT,
            user TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_log(event_type, path, user="Desconhecido"):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (timestamp, event_type, path, user)
        VALUES (?, ?, ?, ?)
    """, (datetime.now().isoformat(), event_type, path, user))
    conn.commit()
    conn.close()

def fetch_logs(period=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if period:
        cursor.execute("SELECT * FROM logs WHERE timestamp >= ?", (period,))
    else:
        cursor.execute("SELECT * FROM logs")
    results = cursor.fetchall()
    conn.close()
    return results
