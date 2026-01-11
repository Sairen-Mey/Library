from __future__ import annotations
import sqlite3
from pathlib import Path
import os

DB_PATH = Path("../data/library.db")

def get_conn() -> sqlite3.Connection:
    print("DB FILE:", os.path.abspath(DB_PATH))
    DB_PATH.parent.mkdir(parents=True,exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1
        );
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            item_id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            is_available INTEGER NOT NULL DEFAULT 1,
            author TEXT, 
            issue TEXT,
            drm INTEGER
        );
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id TEXT NOT NULL,
            item_id TEXT NOT NULL,
            checkout_at TEXT NOT NULL,
            due_date TEXT NOT NULL,
            returned_at TEXT,
            FOREIGN KEY(member_id) REFERENCES members(member_id),
            FOREIGN KEY(item_id) REFERENCES items(item_id)
        );
        """)
        conn.commit()

def seed_db():
    with get_conn() as conn:
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
