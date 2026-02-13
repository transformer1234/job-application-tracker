import sqlite3
from pathlib import Path

DB_PATH = Path("data/applications.db")


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            date_applied TEXT,
            status TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()
