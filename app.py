from flask import Flask, jsonify, request, abort
from library import Library
from models import Book, Magazine, EBook, Member
import sqlite3
from pathlib import Path

DB_PATH = Path("library.db")

app = Flask(__name__)


lib = Library()

# book = Book("0","da", "unknown")
# a = Member("0", "hahah3a",0,[])
# b = Member("1", "hah2aha",1,[])
# c = Member("2", "h1ahaha",1,[])
# lib.add_member(a)
# lib.add_member(b)
# lib.add_member(c)
# lib.add_item(book)
# lib.checkout_item("2","0")


def load_from_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        for row in conn.execute("SELECT member_id, name, active FROM members;").fetchall():
            lib.add_member(Member(row["member_id"], row["name"], bool(row["active"])))

        for row in conn.execute("SELECT item_id, type, title, author, issue, drm FROM items;").fetchall():
            t = row["type"].lower()
            if t == "book":
                lib.add_item(Book(row["item_id"], row["title"], row["author"] or "Unknown"))
            elif t == "magazine":
                lib.add_item(Magazine(row["item_id"], row["title"], row["issue"] or "unknown"))
            elif t == "ebook":
                lib.add_item(EBook(row["item_id"], row["title"], bool(row["drm"])))


@app.get("/members/")
def get_members():
    return jsonify([m for m in lib._members.values()])

@app.get("/members/<member_id>")
def get_member(member_id:str):
    return jsonify(lib.get_member(member_id))

@app.get("/members/<member_id>/items")
def get_member_items(member_id:str):
    return jsonify([item.to_dict() for item in lib.list_member_items(member_id)])

@app.get("/items/<item_id>")
def get_item(item_id:str):
    return jsonify([lib.get_item(item_id).to_dict()])

if __name__ == '__main__':
    app.run(debug=True)