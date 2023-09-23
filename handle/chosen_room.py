from flask import request, session
from handle.room_manager import rooms, ROOM_CODE_LENGTH, generate_room_code
from mongo.mongo import create_collection

def create_custom_room(room_chosen):
    name = request.form.get("name")
    
    if room_chosen == 'roomA':
        room = 'custom-room-A-secret-code-room-123456'
    elif room_chosen == 'roomB':
        room = 'custom-room-B-secret-code-room-123456'
    elif room_chosen == 'roomC':
        room = 'custom-room-C-secret-code-room-123456'
    else:
        room = 'custom-room-D-secret-code-room-123456'

    rooms[room] = {"members": 0, "messages": []}
    
    session["room"] = room
    session["name"] = name
    
    create_collection(room)
    
    return "views.custom_room"



def handle_create():
    
    name = request.form.get("name")
    
    room = generate_room_code(ROOM_CODE_LENGTH)
    rooms[room] = {"members": 0, "messages": []}
    
    session["room"] = room
    session["name"] = name
    
    create_collection(room)
    
    return "views.room"