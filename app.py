from flask import Flask, session, request, redirect, url_for, render_template 
from flask_socketio import SocketIO, join_room, send, leave_room  
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "youwontguessthiskey"
socketio = SocketIO(app)
rooms = {}


def generate_room_code(code_length):
    while True:
        code = ""
        for _ in range(code_length):
            code += random.choice(ascii_uppercase)
            
        if code not in rooms:
            break
        
    print(code)    
    return code


@app.route("/", methods=['POST', 'GET'])
def home():
    
    session.clear()
    
    if request.method == "POST":
        name = request.form.get("name")
        room_code = request.form.get("room_code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        
        if not name:
            return render_template("home.html", error="Please enter a name",name=name, code=room_code) 
        
        if join != False and not room_code:
            return render_template("home.html", error="Please enter a room code",name=name, code=room_code)
        
        room = room_code
        
        if create != False:
            room = generate_room_code(5)
            rooms[room] = {"members": 0,"messages": []}
            
        elif room_code not in rooms:
            return render_template("home.html", error="Rooms does not exist",name=name, code=room_code)
                        
        
        session["room"] = room
        session["name"] = name
        
        return redirect( url_for("room"))
        
        
    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])


#sace here messages in SQL
@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    
    content = {"name": session.get("name"), 
               "message": data["data"]}
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")


@socketio.on("connect") 
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has enterd the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")
    
    
@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")



if __name__ == "__main__":
    socketio.run(app=app, debug=True)