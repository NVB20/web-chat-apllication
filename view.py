from flask import Blueprint, session, request, redirect, url_for, render_template 
from input_checks.check_name import validate_name
from input_checks.chosen_room import handle_create, handle_openpy
from room_manager import rooms

view = Blueprint("views", __name__, static_folder="static", template_folder="templates")




@view.route("/", methods=['POST', 'GET'])
def home():
    
    session.clear()
    
    if request.method == "POST":
        name = request.form.get("name")
        room_code = request.form.get("room_code")
        print("pythn", request.form.get("openpy")) 
        print("craewte" ,request.form.get("create")) 
              
        error = validate_name()          
        if error:
            return render_template("home.html", error=error, name=name, room_code=room_code)

        room = room_code  
              
        if request.form.get("openpy"):
            route = handle_openpy() 
            print("this is the route: ", route)
            return redirect(url_for(route))       
   
        if request.form.get("create"):
            route = handle_create()
            print("this is the route: ", route)
            return redirect(url_for(route))

        if room_code and room_code not in rooms:
            return render_template("home.html", error="Room does not exist", name=name, room_code=room_code)  
                      
        session["room"] = room
        session["name"] = name
        
        return redirect( url_for("views.room"))
        
        
    return render_template("home.html")

@view.route("/room")
def room():
    name = session.get("name")
    room = session.get("room")
    if room is None or name is None or room not in rooms:
        return redirect(url_for("views.home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"], name=name)


@view.route("/python_room")
def python_room():
    name = session.get("name")
    room = session.get("room")
    if room is None or name is None or room not in rooms:
        return redirect(url_for("views.home"))

    return render_template("python-room.html", code=room, messages=rooms[room]["messages"],  room_type="Python", name=name)


