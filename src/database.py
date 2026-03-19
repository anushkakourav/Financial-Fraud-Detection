# src/database.py

import sqlite3
from src.config import DATABASE_PATH


def get_connection():
    """Create SQLite connection"""
    return sqlite3.connect(DATABASE_PATH)


def create_table():
    """Create transactions table if it does not exist"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trans_num TEXT,
        cc_num TEXT,
        amt REAL,
        category TEXT,
        prediction INTEGER,
        probability REAL,
        risk_level TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def insert_transaction(data, prediction, probability, risk_level):
    """Insert processed transaction with prediction result"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions 
    (trans_num, cc_num, amt, category, prediction, probability, risk_level)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("trans_num", "N/A"),
        data.get("cc_num", "N/A"),
        data.get("amt", 0.0),
        data.get("category", "unknown"),
        int(prediction),
        float(probability),
        risk_level
    ))

    conn.commit()
    conn.close()