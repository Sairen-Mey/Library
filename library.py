from models import LibraryItem, Member
from typing import Optional
from datetime import datetime

class Library:
    def __init__(self):
        self._items: dict[str, LibraryItem] = {}
        self._members: dict[str, Member] = {}

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