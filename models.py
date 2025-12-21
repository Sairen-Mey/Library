from dataclasses import field
from typing import Optional
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from dataclasses import dataclass


class LibraryItem(ABC):
    def __init__(self, item_id:str, title:str):
        self._id = item_id
        self._title = title
        self._is_available: bool = True
        self._borrowed_id: Optional[str] = None
        self._due_date: Optional[datetime] = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def is_available(self) -> bool:
        return self._is_available

    @property
    def borrowed_id(self) -> Optional[str]:
        return self._borrowed_id

    @property
    def due_date(self)-> Optional[datetime]:
        return self._due_date


    @abstractmethod
    def loan_period(self) -> timedelta:
        pass

    def checkout(self, member_id: str) -> bool:
        if self._is_available:
            self._borrowed_id = member_id
            self._due_date = datetime.now() + self.loan_period()
            self._is_available = False
            return True
        else:
            return False


    def return_item(self) -> bool:
        if self._is_available == False:
            self._is_available = True
            self._borrowed_id = None
            self._due_date = None
            return True
        else:
            return False

    @abstractmethod
    def to_dict(self):
        pass


class Book(LibraryItem):
    def __init__(self, item_id:str, title:str, author:str):
        super().__init__(item_id, title)
        self._author = author

    @property
    def author(self):
        return self._author


    def loan_period(self) -> timedelta:
        return timedelta(days=14)

    def to_dict(self):
        return {"id":self._id, "title":self.title, "author":self._author}


class Magazine(LibraryItem):
    def __init__(self, item_id: str, title: str, issue: str):
        super().__init__(item_id, title)
        self._issue = issue

    @property
    def issue(self):
        return self._issue

    def loan_period(self) -> timedelta:
        return timedelta(days=7)

    def to_dict(self):
        return {"id": self._id, "title": self.title, "issue": self._issue}


class EBook(LibraryItem):
    def __init__(self, item_id: str, title: str, drm: bool):
        super().__init__(item_id, title)
        self._drm = drm

    @property
    def issue(self):
        return self._drm

    def loan_period(self) -> timedelta:
        return timedelta(days=21)

    def to_dict(self):
        return {"id": self._id, "title": self.title, "drm": self._drm}


@dataclass
class Member:
    member_id : str
    name : str
    active : bool = True
    borrowed_ids : list[str] = field(default_factory=list)

    def to_dict(self):
        return {"id":self.member_id, "name":self.name, "active":self.active, "borowed_ids":self.borrowed_ids}