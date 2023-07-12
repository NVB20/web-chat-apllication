from flask import Flask, Blueprint, session, request, redirect, url_for, render_template 
from flask_socketio import SocketIO, join_room, send, leave_room  
import random
from string import ascii_uppercase
rooms = {}

view = Blueprint("views", __name__, static_folder="static", template_folder="templates")
ROOM_CODE_LENGTH = 11

def generate_room_code(ROOM_CODE_LENGTH):
    while True:
        code = ""
        for _ in range(ROOM_CODE_LENGTH):
            code += random.choice(ascii_uppercase)
            
        if code not in rooms:
            break
        
    print(code)    
    return code



@view.route("/", methods=['POST', 'GET'])
def home():
    
    session.clear()
    
    if request.method == "POST":
        name = request.form.get("name")
        room_code = request.form.get("room_code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        openpy = request.form.get("openpy", False)                              
                  
        if not name:
            return render_template("home.html", error="Please enter a name", name=name, room_code=room_code) 
        
        if len(name) <= 2:
            return render_template("home.html", error="Name must be longer than 2", name=name, room_code=room_code) 
                    
        if join != False and not room_code:
            return render_template("home.html", error="Please enter a room code", name=name, room_code=room_code)
        
        room = room_code 
        
        if openpy != False:
            print("openpy got clicked on!", openpy)
            python_room = "SBSOVMQFEJJ"
            rooms["SBSOVMQFEJJ"] = {"members": 0,"messages": []}    
                              
            session["room"] = python_room
            session["name"] = name
                        
            return redirect( url_for("views.python_room"))
              
              
        #create button generate new room code
        if create != False:
            print("enter from the create button")
            room = generate_room_code(ROOM_CODE_LENGTH)
            rooms[room] = {"members": 0,"messages": []}     
        elif room_code not in rooms:
            return render_template("home.html", error="Rooms does not exist",name=name , room_code=room_code)
                        
        
        session["room"] = room
        session["name"] = name
        
        return redirect( url_for("views.room"))
        
        
    return render_template("home.html")


@view.route("/python_room")
def python_room():
    openpy = request.form.get("openpy", False)
    name = session.get("name")
    room = session.get("room")
    if room is None or name is None or room not in rooms:
        return redirect(url_for("views.home"))

    return render_template("python-room.html", code=room, messages=rooms[room]["messages"],  room_type="Python", name=name)


@view.route("/room")
def room():
    openpy = request.form.get("openpy", False)
    name = session.get("name")
    room = session.get("room")
    if room is None or name is None or room not in rooms:
        return redirect(url_for("views.home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"], name=name)


