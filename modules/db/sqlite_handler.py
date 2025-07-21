import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "cases.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lagrum TEXT NOT NULL,
            beskrivning TEXT,
            datum TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS publiceringar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            innehåll TEXT,
            datum TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS logg (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meddelande TEXT,
            tid TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_case(lagrum, beskrivning, datum):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO cases (lagrum, beskrivning, datum) VALUES (?, ?, ?)", (lagrum, beskrivning, datum))
    conn.commit()
    conn.close()

def save_publicering(case_id, innehåll, datum):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO publiceringar (case_id, innehåll, datum) VALUES (?, ?, ?)", (case_id, innehåll, datum))
    conn.commit()
    conn.close()

def get_case_by_lagrum(lagrum):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM cases WHERE lagrum = ?", (lagrum,))
    row = c.fetchone()
    conn.close()
    return row

def list_cases():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, lagrum, beskrivning, datum FROM cases")
    rows = c.fetchall()
    conn.close()
    return rows

def log_event(meddelande, tid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO logg (meddelande, tid) VALUES (?, ?)", (meddelande, tid))
    conn.commit()
    conn.close()
