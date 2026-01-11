from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from .db import get_conn


def db_list_members():
    with get_conn() as conn:
        return conn.execute("SELECT member_id, name, active FROM members;").fetchall()

def db_get_member(member_id:str):
    with get_conn() as conn:
        return conn.execute(
            "SELECT member_id, name, active FROM members WHERE member_id = ?;",
            (member_id,),
        ).fetchall()

def db_create_member(member_id:str, name:str, active:bool = True) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO members(member_id, name, active) VALUES (?,?,?);",
            (member_id,name,1 if active else 0),
        )
        conn.commit()

def db_list_items(item_type: Optional[str] = None):
    with get_conn() as conn:
        if item_type:
            return conn.execute("SELECT * FROM items WHERE type = ?;",
                                (item_type.lower(),)).fetchall()
        return conn.execute(
            "SELECT * FROM items;"
        ).fetchall()

def db_get_item(item_id:str):
    with get_conn() as conn:
        return conn.execute(
            "SELECT item_id, title, is_available, author, issue, drm FROM items WHERE item_id = ?;",
            (item_id,),
        ).fetchall()
"""    """
def db_create_item(item_id:str, type:str, title:str, is_available:bool, author = None, issue = None, drm = None):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO items(item_id, type, title, is_available, author, issue, drm) VALUES (?,?,?,?,?,?);",
            (item_id, type.lower(), title, 1 if is_available else 0,author,issue,drm)
        )
        conn.commit()

def db_has_open_loan(item_id:str) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT 1 FROM loans WHERE item_id = ? AND returned_at IS NULL LINIT 1;",
            (item_id,),
        ).fetchall()
        return row is not None

def db_member_open_loans(member_id:str):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM loans WHERE member_id = ? AND returned_at IS NULL;",
            (member_id,),
        ).fetchall()

def db_checkout(member_id:str, item_id:str, due_date_iso:str) -> None:
    now_iso = datetime.now().isoformat(timespec="seconds")
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO loans(member_id, item_id, checkout_at, due_date, returned_at)
            VALUES (?,?,?,?,NULL);
            """,
                     (member_id,item_id,now_iso,due_date_iso),
        )
        conn.commit()

def db_return(member_id:str, item_id:str) -> bool:
    new_iso = datetime.now().isoformat(timespec="seconds")
    with get_conn() as conn:
        cur = conn.execute("""
            UPDATE loans
            SET returned_at = ?
            WHERE member_id = ? AND item_id = ? AND returned_at IS NULL;    
            """,
            (new_iso,member_id,item_id),
        )
    conn.commit()
    return cur.rowcount > 0
