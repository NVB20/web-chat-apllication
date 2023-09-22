from flask import request, session
from room_manager import rooms, ROOM_CODE_LENGTH, generate_room_code
from mongo.mongo import create_collection

def handle_openpy():
    print("openpy got clicked on!")
    name = request.form.get("name")
    
    python_room = "SBSOVMQFEJJ"
    rooms[python_room] = {"members": 0, "messages": []}
    
    session["room"] = python_room
    session["name"] = name

    create_collection(python_room)
    
    return "views.python_room"


def handle_create():
    print("enter from the create button")
    name = request.form.get("name")
    
    room = generate_room_code(ROOM_CODE_LENGTH)
    rooms[room] = {"members": 0, "messages": []}
    
    session["room"] = room
    session["name"] = name
    
    create_collection(room)
    
    return "views.room"