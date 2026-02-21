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
    reassign_ids()  # Reset IDs after deletion



def get_filtered_applications(
    status: str = None,
    search: str = None,
    date_from: str = None,
    date_to: str = None,
    sort_by: str = "date_applied",
    sort_order: str = "DESC",
    page: int = 1,
    page_size: int = 10
):
    conn = get_connection()
    cursor = conn.cursor()

    allowed_sort_columns = {"date_applied", "company", "role", "status"}
    if sort_by not in allowed_sort_columns:
        sort_by = "date_applied"
    sort_order = "ASC" if sort_order.upper() == "ASC" else "DESC"

    query = "SELECT * FROM applications WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)

    if search:
        query += " AND (company LIKE ? OR role LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    if date_from:
        query += " AND date_applied >= ?"
        params.append(date_from)

    if date_to:
        query += " AND date_applied <= ?"
        params.append(date_to)

    # Count total for pagination
    count_cursor = conn.cursor()
    count_cursor.execute(query.replace("SELECT *", "SELECT COUNT(*)"), params)
    total_count = count_cursor.fetchone()[0]

    query += f" ORDER BY {sort_by} {sort_order}"
    query += " LIMIT ? OFFSET ?"
    params.extend([page_size, (page - 1) * page_size])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows, total_count


def reassign_ids():
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch all rows ordered by current id
    cursor.execute("SELECT * FROM applications ORDER BY id ASC")
    rows = cursor.fetchall()

    # Delete all rows
    cursor.execute("DELETE FROM applications")

    # Re-insert with new sequential IDs
    for new_id, row in enumerate(rows, start=1):
        cursor.execute("""
            INSERT INTO applications (id, company, role, location, date_applied, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (new_id, row[1], row[2], row[3], row[4], row[5], row[6]))

    # Reset SQLite auto-increment counter
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='applications'")
    cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('applications', ?)", (len(rows),))

    conn.commit()
    conn.close()