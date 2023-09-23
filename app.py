from flask import Flask, session
from flask_socketio import SocketIO, join_room, send, leave_room  
from view import view
from handle.room_manager import rooms, SCECRET_KEY
from handle.handle_time import time_now
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = SCECRET_KEY
socketio = SocketIO(app)
app.register_blueprint(view, url_prefix="")

# Dictionary to track client disconnections
disconnect_flags = {}

from mongo.mongo import insert_messages_to_mongo, delete_collection
@socketio.on("message")
def message(data):
    room = session.get("room")
    
    if room not in rooms:
        return 
    
    content = {"name": session.get("name"), 
               "message": data["data"],
               "time": time_now()
               }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    
    insert_messages_to_mongo(content, room)
    
    time = time_now()
    print(f"{session.get('name')} said: {data['data']} at: {time}")


@socketio.on("connect") 
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    time = time_now()
    
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has enterd the room", "time": time}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room} {time}")  


@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name", False)
    time = time_now()
    
    print("socket emitted here")
    
    if room in rooms:
        rooms[room]['members'] -= 1
        if rooms[room]['members'] <= 0:
            del rooms[room]
            delete_collection(room)
            print("delted room from lists")
    
    send({"name": name, "message": "has left the room", "time": time}, to=room, name=name)
    print(f"{name} has left the room {room} {time}")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app=app, debug=True,host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
