from flask import Flask, session, request, redirect, url_for, render_template 
from flask_socketio import SocketIO, join_room, send, leave_room  
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = "youwontguessthiskey"
socketio = SocketIO(app)
rooms = {}
# Dictionary to track client disconnections
disconnect_flags = {}
ROOM_CODE_LENGTH = 11
#python room
rooms["SBSOVMQFEJJ"] = {"members": 0, "messages": []}
#java room
rooms["JFVRWQHEDRG"] = {"members": 0, "messages": []}
#devops room
rooms["HVXNDLUNQFD"] = {"members": 0, "messages": []}
#java script
rooms["ETGTUAOWFTS"] = {"memberes": 0, "messages": []}

def generate_room_code(ROOM_CODE_LENGTH):
    while True:
        code = ""
        for _ in range(ROOM_CODE_LENGTH):
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
        openpy = request.form.get("openpy", False)
        openjava = request.form.get("java", False)
        opendevops = request.form.get("devops", False)
        openjavascript = request.form.get("javascript", False)  
                               
                  
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
                        
            return redirect( url_for("python_room"))
            
        if openjava != False:
            room = "JFVRWQHEDRG"
            rooms["JFVRWQHEDRG"] = {"members": 0,"messages": []}
            
            session["room"] = room
            session["name"] = name
            
            return redirect( url_for("java_room"))  
        
        if opendevops != False:
            room = "HVXNDLUNQFD"
            rooms[room] = {"members": 0,"messages": []}
            
            session["room"] = room
            session["name"] = name
            
            return redirect( url_for("devops_room"))   
        
        if openjavascript != False:
            room = generate_room_code(ROOM_CODE_LENGTH)
            rooms[room] = {"members": 0,"messages": []}
            session["room"] = room
            session["name"] = name
            
            return redirect( url_for("javascript_room"))  
              
        #create button create new room 
        if create != False:
            print("enter from the create button")
            room = generate_room_code(ROOM_CODE_LENGTH)
            rooms[room] = {"members": 0,"messages": []}     
        elif room_code not in rooms:
            return render_template("home.html", error="Rooms does not exist",name=name, room_code=room_code)
                        
        
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


@app.route("/python_room")
def python_room():
    openpy = request.form.get("openpy", False)
    print(openpy)
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("python-room.html", code=room, messages=rooms[room]["messages"],  room_type="Python")


@app.route("/java_room")
def java_room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("java-room.html", code=room, messages=rooms[room]["messages"])


@app.route("/devops_room")
def devops_room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("devops-room.html", code=room, messages=rooms[room]["messages"])


@app.route("/javascript_room")
def javascript_room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("javascript-room.html", code=room, messages=rooms[room]["messages"])


#save here messages in SQL
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
def handle_disconnect():
    room = session.get("room")
    name = session.get("name", False)
    
    # Check if disconnection is intentional or due to refresh
    if disconnect_flags.get(request.sid):
        leave_room(room)

        if room in rooms:
            rooms[room]['members'] -= 1
            if rooms[room]['members'] <= 0:
                del rooms[room]
                
        
        # Remove the disconnect flag for this client
        del disconnect_flags[request.sid]
    else:
        # Set the disconnect flag for this client
        disconnect_flags[request.sid] = True
       
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


if __name__ == "__main__":
    socketio.run(app=app, debug=True)