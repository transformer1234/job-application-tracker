import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id SERIAL PRIMARY KEY,
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