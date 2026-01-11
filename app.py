from __future__ import annotations
from flask import Flask, jsonify, abort, request
from library_service.library import Library
from library_service.db import init_db


app = Flask(__name__)


lib = Library()
init_db()

def require_json() -> dict:
    if not request.is_json:
        abort(400, description="Request body must be JSON")
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Invalid JSON")
    return data

@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(err):
    return jsonify({"error":err.description}), err.code

@app.get("/members")
def get_members():
    return jsonify([m.to_dict() for m in lib.list_members()])

@app.post("/members")
def create_member():
    data = require_json()
    member_id = data.get("member_id")
    name = data.get("name")
    if not member_id or not name:
        abort(400, description="Invalid member_id or name")
    try:
        m = lib.create_member(member_id,name)
        return jsonify(m.to_dict()), 201
    except Exception as e:
        abort(404,description=str(e))


@app.get("/members/<member_id>")
def get_member(member_id:str):
     m = lib.get_member(member_id)
     if not m:
         abort(404, description="Invalid member id")
     return jsonify(m.to_dict())



@app.get("/members/<member_id>/items")
def get_member_items(member_id:str):
    return jsonify([item.to_dict() for item in lib.list_member_items(member_id)])

@app.get("/items/<item_id>")
def get_item(item_id:str):
    return jsonify([lib.get_item(item_id).to_dict()])

@app.post("/items")
def create_item():
    data = require_json()
    try:
        m = lib.create_item(data)
        return jsonify(m.to_dict()), 201
    except Exception as e:
        abort(400, description=str(e))

@app.get("/items")
def list_items():
    t = request.args.get("type")
    return jsonify([m.to_dict() for m in lib.list_items(t)])


@app.post("/checkout")
def checkout():
    data = require_json()
    member_id = data.get("member_id")
    item_id = data.get("item_id")

    if not member_id or not item_id :
        abort(400, description="Invalid member_id or item_id")

    try:
        res = lib.checkout_item(member_id,item_id)
        return jsonify({"massage":"checked out", **res})
    except Exception as e:
        abort(404, description=str(e))


@app.post("/return")
def return_item():
    data = require_json()
    member_id = data.get("member_id")
    item_id = data.get("item_id")

    if not member_id or not item_id :
        abort(400, description="Invalid member_id or item_id")

    try:
        lib.return_item(member_id,item_id)
        return jsonify({"massage":"successful returned"})
    except Exception as e:
        abort(404, description=str(e))




if __name__ == '__main__':
    app.run(debug=True)