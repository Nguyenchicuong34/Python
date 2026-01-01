import sqlite3
import hashlib

DB_NAME = 'study_mate_pro.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Các bảng cũ
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, role TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, uploader TEXT, title TEXT, file_path TEXT, description TEXT)')
    
    # --- CÁC BẢNG MỚI ---
    # Bảng Ghi chú
    c.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, username TEXT, content TEXT, timestamp TEXT)')
    # Bảng Sự kiện/Deadline
    c.execute('CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, username TEXT, event_name TEXT, event_date TEXT)')
    
    conn.commit()
    conn.close()

# --- USER ---
def register_user(u, p, role="user"):
    conn = sqlite3.connect(DB_NAME)
    try:
        hashed = hashlib.sha256(p.encode()).hexdigest()
        conn.execute("INSERT INTO users VALUES (?, ?, ?)", (u, hashed, role))
        conn.commit()
        return True
    except: return False
    finally: conn.close()

def login_user(u, p):
    conn = sqlite3.connect(DB_NAME)
    hashed = hashlib.sha256(p.encode()).hexdigest()
    cur = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (u, hashed))
    res = cur.fetchone()
    conn.close()
    return res

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    res = conn.execute("SELECT username, role FROM users").fetchall()
    conn.close()
    return res

# --- DOCUMENT ---
def share_document(uploader, title, path, desc):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO documents (uploader, title, file_path, description) VALUES (?, ?, ?, ?)", (uploader, title, path, desc))
    conn.commit()
    conn.close()

def get_all_documents():
    conn = sqlite3.connect(DB_NAME)
    res = conn.execute("SELECT * FROM documents").fetchall()
    conn.close()
    return res

# --- NOTES (MỚI) ---
def add_note(user, content):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO notes (username, content, timestamp) VALUES (?, ?, datetime('now', 'localtime'))", (user, content))
    conn.commit()
    conn.close()

def get_notes(user):
    conn = sqlite3.connect(DB_NAME)
    res = conn.execute("SELECT * FROM notes WHERE username=?", (user,)).fetchall()
    conn.close()
    return res

def delete_note(id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()

# --- EVENTS (MỚI) ---
def add_event(user, name, date):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO events (username, event_name, event_date) VALUES (?, ?, ?)", (user, name, date))
    conn.commit()
    conn.close()

def get_events(user):
    conn = sqlite3.connect(DB_NAME)
    res = conn.execute("SELECT * FROM events WHERE username=?", (user,)).fetchall()
    conn.close()
    return res

def delete_event(id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM events WHERE id=?", (id,))
    conn.commit()
    conn.close()