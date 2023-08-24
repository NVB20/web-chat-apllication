import re
from flask import request


def validate_name():
    name = request.form.get("name")    
    join = request.form.get("join", False)
    room_code = request.form.get("room_code")
    
    if not name:
        return "Please enter a name"
          
    if len(name) <= 2:
        return "Name must be longer than 2 charcters"
    
    if len(name) > 6:
        return "Name cant be longer than 6 charcters"
    
    if not re.match("^[a-zA-Z0-9]+$", name):
        return "Name can only contain letters and numbers"
    
    if join and not room_code:
            return "Please enter a room code"
    
    return None
