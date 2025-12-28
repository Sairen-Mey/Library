from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from .models import Book, Magazine, EBook, LibraryItem, Member
from . import services as ser

class Library:
    def list_members(self) -> List[Member]:
        rows = ser.db_list_members()
        return [Member(r[0],r[1],bool(r[2])) for r in rows]

    def list_items(self, item_type:str) -> List[LibraryItem]:
        rows = ser.db_list_items(item_type)
        return [LibraryItem(r[0]) for r in rows]



    def add_item(self, item: LibraryItem) -> None:
        if item._id in self._items:
            raise ValueError("Item with this id already exists")
        self._items[item._id] = item

    def add_member(self, member: Member) -> None:
        if member.member_id in self._members:
            raise ValueError("Member with this id already exists")
        self._members[member.member_id] = member

    def get_item(self, item_id: str) -> Optional[LibraryItem]:
        return self._items.get(item_id)

    def get_member(self, member_id: str) -> Optional[Member]:
        return self._members.get(member_id)

    def checkout_item(self, member_id: str, item_id: str) -> bool:
        member = self.get_member(member_id)
        item = self.get_item(item_id)

        if member is None or not member.active:
            return False
        if item is None or item not in self._items.values():
            return False
        if item_id in member.borrowed_ids:
            return False

        ok = item.checkout(member_id)
        if ok:
            member.borrowed_ids.append(item_id)
            return True
        return False

    def return_item(self, member_id: str, item_id: str) -> bool:
        member = self.get_member(member_id)
        item = self.get_item(item_id)

        if member is None or item is None:
            return False
        if item_id not in member.borrowed_ids:
            return False

        ok = item.return_item()
        if ok:
            member.borrowed_ids.remove(item_id)
            return True
        return False

    def list_member_items(self, member_id: str):
        member = self.get_member(member_id)
        if member is None:
            return []
        return [self._items[i] for i in member.borrowed_ids if i in self._items]

    def list_overdue_items(self, now: Optional[datetime] = None):
        if now is None:
            now = datetime.now()
        result: list[LibraryItem] = []
        for item in self._items.values():
            if item.due_date is not None and item.due_date < now and not item.is_available:
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