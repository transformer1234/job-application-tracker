from typing import List, Optional
from backend.database import get_connection
from backend.models import ApplicationCreate


def create_application(app: ApplicationCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applications (company, role, location, date_applied, status, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        app.company,
        app.role,
        app.location,
        app.date_applied.isoformat(),
        app.status,
        app.notes
    ))

    conn.commit()
    app_id = cursor.lastrowid
    conn.close()
    return app_id


def get_all_applications():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications ORDER BY date_applied DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_application_by_id(app_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM applications WHERE id = ?", (app_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row


def update_application_status(app_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE applications SET status = ? WHERE id = ?",
        (status, app_id)
    )
    conn.commit()
    conn.close()


def delete_application(app_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM applications WHERE id = ?",
        (app_id,)
    )
    conn.commit()
    conn.close()
