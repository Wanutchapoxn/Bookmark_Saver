import sqlite3
from werkzeug.security import generate_password_hash

DB_NAME = "bookmarks.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    with get_connection() as conn:
        c = conn.cursor()

        # ตาราง categories
        c.execute('''CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL
                    )''')

        # ตาราง bookmarks
        c.execute('''CREATE TABLE IF NOT EXISTS bookmarks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        url TEXT NOT NULL,
                        category TEXT,
                        created_at TEXT
                    )''')

        # ตาราง users
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )''')

        # category เริ่มต้น
        c.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", ("Other",))

        # user เริ่มต้น (admin / 1234)
        c.execute("SELECT * FROM users WHERE username=?", ("admin",))
        if not c.fetchone():
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (
                "admin",
                generate_password_hash("1234")
            ))

        conn.commit()


# ===== helper functions สำหรับ User =====
def get_user_by_username(username):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id, username, password FROM users WHERE username=?", (username,))
        return c.fetchone()


def get_user_by_id(user_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id, username, password FROM users WHERE id=?", (user_id,))
        return c.fetchone()
def get_connection():
    return sqlite3.connect(DB_NAME)


def create_user(username, password):
    with get_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (
                username,
                generate_password_hash(password)
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # username ซ้ำ
            return False


def get_user_by_username(username):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id, username, password FROM users WHERE username=?", (username,))
        return c.fetchone()


def get_user_by_id(user_id):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id, username, password FROM users WHERE id=?", (user_id,))
        return c.fetchone()