import re
from flask import request, render_template


def validate_name():
    name = request.form.get("name")    
    
    if not name:
        return "Please enter a name"
          
    if len(name) <= 2:
        return "Name must be longer than 2 charcters"
    
    if len(name) > 10:
        return "Name cant be longer than 10 charcters"
    
    if not contains_symbols(name):
        return "Name cant contain symbols"
                        
    
    return None

def contains_symbols(name):
    pattern = r'^[a-zA-Z0-9]+$'
    return re.match(pattern, name) is not None