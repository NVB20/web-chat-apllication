from flask import Blueprint, session, request, redirect, url_for, render_template 
from input_checks.check_name import validate_name
from input_checks.chosen_room import handle_create, handle_openpy
from input_checks.valid_login_inputs import is_valid_email, check_password, check_user_exists
from mongo.sign import register_user, user_login
from room_manager import rooms
from mongo.mongo import retrieve_message_history


view = Blueprint("views", __name__, static_folder="static", template_folder="templates")

@view.route("/home", methods=['POST', 'GET'])
def home():
    
    session.clear()
    
    if request.method == "POST":
        name = request.form.get("name")
        room_code = request.form.get("room_code")
              
        error = validate_name()          
        if error:
            return render_template("home.html", error=error, name=name, room_code=room_code)

        room = room_code  
              
        if request.form.get("openpy"):
            return redirect(url_for(handle_openpy() ))       
   
        if request.form.get("create"):
            return redirect(url_for(handle_create()))

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


@view.route("/get_messages")
def get_messages():
    all_messages = retrieve_message_history(session["room"])
    return all_messages

@view.route("/")
@view.route("/login", methods=['POST', 'GET'])
def login():

    session.clear()

    if request.method == "POST":
        
        if request.form.get("register"):
            email = request.form.get("email")
            password = request.form.get("password")
            print("clicked register")

        
            
            if is_valid_email(email) is not None:
                error = is_valid_email(email)
                return render_template("login.html", error=error)
            if check_password(password) is not None:
                error = check_password(password)
                return render_template("login.html", error=error)
            if check_user_exists(email) is True:
                error = "user already exists"
                return render_template("login.html", error=error)

            register_user()
            return redirect( url_for("views.home"))

        if request.form.get("login"):    

            if user_login() is False:
                error = "User doesn't exist or incorrect password"
                return render_template("login.html", error=error)
        
            return redirect( url_for("views.home"))

    return render_template("login.html")