import sqlite3
from datetime import datetime


# ==========================================
# 🚔 POLICEAI DATABASE
# ==========================================

DATABASE_NAME = "policeai.db"


# ==========================================
# Create Database
# ==========================================

def create_database():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            complaint TEXT NOT NULL,

            crime_type TEXT NOT NULL,

            priority TEXT NOT NULL,

            location TEXT,

            incident_date TEXT NOT NULL,

            incident_time TEXT NOT NULL,

            status TEXT NOT NULL

        )
    """)

    connection.commit()

    connection.close()


# ==========================================
# Add Incident
# ==========================================

def add_incident(
    complaint,
    crime_type,
    priority,
    location=""
):

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    now = datetime.now()

    incident_date = now.strftime(
        "%Y-%m-%d"
    )

    incident_time = now.strftime(
        "%H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO incidents
        (
            complaint,
            crime_type,
            priority,
            location,
            incident_date,
            incident_time,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        complaint,
        crime_type,
        priority,
        location,
        incident_date,
        incident_time,
        "Pending"
    ))

    connection.commit()

    incident_id = cursor.lastrowid

    connection.close()

    return incident_id


# ==========================================
# Get All Incidents
# ==========================================

def get_incidents():

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            complaint,
            crime_type,
            priority,
            location,
            incident_date,
            incident_time,
            status
        FROM incidents
        ORDER BY id DESC
    """)

    incidents = cursor.fetchall()

    connection.close()

    return incidents


# ==========================================
# Update Incident Status
# ==========================================

def update_status(
    incident_id,
    new_status
):

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE incidents
        SET status = ?
        WHERE id = ?
    """, (
        new_status,
        incident_id
    ))

    connection.commit()

    connection.close()


# ==========================================
# Initialize Database
# ==========================================

create_database()

def add_emergency_alert(emergency_type, location, description, priority):

    conn = sqlite3.connect("policeai.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emergency_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emergency_type TEXT,
            location TEXT,
            description TEXT,
            priority TEXT,
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO emergency_alerts
        (emergency_type, location, description, priority)
        VALUES (?, ?, ?, ?)
    """, (
        emergency_type,
        location,
        description,
        priority
    ))

    conn.commit()
    alert_id = cursor.lastrowid
    conn.close()

    return alert_id

def get_emergency_alerts():

    conn = sqlite3.connect("policeai.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, emergency_type, location,
               description, priority, status, created_at
        FROM emergency_alerts
        ORDER BY id DESC
    """)

    alerts = cursor.fetchall()

    conn.close()

    return alerts


def update_emergency_status(alert_id, status):

    conn = sqlite3.connect("policeai.db")

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE emergency_alerts
        SET status = ?
        WHERE id = ?
    """, (status, alert_id))

    conn.commit()

    conn.close()