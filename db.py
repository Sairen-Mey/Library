import sqlite3
from pathlib import Path

DB_PATH = Path("library.db")

def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXIST members (
            member_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1
        );
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXIST items (
            item_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            is_available INTEGER NOT NULL DEFAULT 1,
            author TEXT, 
            issue TEXT,
            drm INTEGER 
        );
        """)

def seed_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM members;")
        conn.execute("DELETE FROM items;")

        members = [
            ("u1", "Ivan", 1),
            ("u2", "Sasha", 1),
            ("u3", "Anton", 0)
        ]

        conn.executemany(
            "INSERT INTO members(member_id, name, active) VALUES (?,?,?)",
            members
        )
        items = [
            ("b1", "book", "Python 101", "Guido", None, None),
            ("b2", "book", "Flask Basics", "Armin", None, None),
            ("b3", "book", "Clean Code", "Robert Martin", None, None),
        ]

        conn.executemany(
            "INSERT INTO items(item_id, type, title, author, issue, drm) VALUES (?, ?, ?, ?, ?, ?);",
            items
        )

        conn.commit()

if __name__ == "__main__":
    init_db()
    seed_db()
    print("DB created and seeded:", DB_PATH.resolve())
