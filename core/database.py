import sqlite3
from core.config import config

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(config.DB_PATH, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS memory (key TEXT PRIMARY KEY, value TEXT)
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, role TEXT, content TEXT)
            """)

    def remember(self, key: str, value: str):
        with self.conn:
            self.conn.execute("INSERT OR REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))

    def get_memory(self, key: str):
        cur = self.conn.cursor()
        cur.execute("SELECT value FROM memory WHERE key=?", (key,))
        row = cur.fetchone()
        return row[0] if row else None

    def log_chat(self, role: str, content: str):
        with self.conn:
            self.conn.execute("INSERT INTO history (role, content) VALUES (?, ?)", (role, content))

db = Database()