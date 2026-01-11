from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from .models import Book, Magazine, EBook, LibraryItem, Member
from . import services as ser

class Library:

    def list_members(self) -> List[Member]:
        rows = ser.db_list_members()
        return [Member(r[0],r[1],bool(r[2])) for r in rows]

    def get_member(self, member_id: str) -> Optional[Member]:
        col = ser.db_get_member(member_id)
        if not col:
            return None
        return Member(col[0],col[1],col[2])

    def create_member(self, member_id:str, name:str) -> Member:
        ser.db_create_member(member_id, name)
        return self.get_member(member_id)

    def list_items(self, item_type:str) -> List[LibraryItem]:
        rows = ser.db_list_items(item_type)
        return [self._row_to_item(r) for r in rows]

    def get_item(self, item_id: str) -> Optional[LibraryItem]:
        row = ser.db_get_item(item_id)
        if not row:
            return None
        return  self._row_to_item(row)

    def create_item(self, payload:dict) -> LibraryItem:
        t = (payload.get("type") or "").lower()
        item_id = payload.get("item_id")
        title = payload.get("title")

        if t == "book":
            author = payload.get("author")
            ser.db_create_item(item_id, t, title, author=author)
        elif t == "magazine":
            issue = payload.get("issue")
            ser.db_create_item(item_id, t, title, issue=issue)
        elif t == "ebook":
            drm = 1 if bool(payload.get("drm")) else 0
            ser.db_create_item(item_id, t, title, drm=drm)
        else:
            raise ValueError("Unknown type")

        return self.get_item(item_id)

    def checkout_item(self, member_id: str, item_id: str) -> dict:
        member = self.get_member(member_id)
        if not member:
            raise ValueError("Member not found")
        if not member.active:
            raise ValueError("Member is not active")

        item = self.get_item(item_id)

        if not item:
            raise ValueError("Item not found")

        if ser.db_has_open_loan(item_id):
            raise ValueError("Item is not available")

        due = datetime.now() + item.loan_period()
        ser.db_checkout(member_id,item_id,due.isoformat(timespec="seconds"))

        return {
            "member_id":member_id,
            "item_id":item_id,
            "due_date":due.isoformat(timespec="seconds"),
        }

    def return_item(self, member_id: str, item_id: str) -> None:
        ok = ser.db_return(member_id, item_id)
        if not ok:
            raise ValueError("no open loan for this mem/item")

    def list_member_items(self, member_id: str) -> List[LibraryItem]:
        loans = ser.db_member_open_loans(member_id)
        result = []
        for l in loans:
            item = self.get_item(l["item_id"])
            if item:
                result.append(item)
        return result

    @staticmethod
    def _row_to_item(row) -> LibraryItem:
        t = (row["type"] or "").lower()
        if t == "book":
            return Book(row["item_id"], row["title"], row["author"] or "Unknown")
        elif t == "magazine":
            return Magazine(row["item_id"], row["title"], row["issue"] or "Unknown")
        elif t == "ebook":
            return EBook(row["item_id"], row["title"], bool(row["drm"]))
        raise ValueError(f"Unknown item type in DB: {row['type']}")
