from flask import request
from pymongo import MongoClient
from mongo.get_mongo_address import get_db_ip_address
import re

IP_ADDRESS = get_db_ip_address('mongodb-service', 'default')

connection_string = f"mongodb://{IP_ADDRESS}/"  
client = MongoClient(connection_string)
users_db = client.users


def check_user_exists(email):
    user = users_db["users"].find_one({"email": email})
    return user is not None

def is_valid_email(email):
    email = request.form.get("email")
    
    if len(email) == 0:
        return "Email cannot be empty"
    
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.(com|co\.il)$'
    if not re.match(pattern, email):
        return "Invalid email format"
    
    return None

def check_password(password):
    password = request.form.get("password")
    
    if len(password) < 8:
        return "Password must be at least 8 characters long"

    # Check for uppercase letter
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter"

    # Check for lowercase letter
    if not any(char.islower() for char in password):
        return "Password must contain at least one lowercase letter"

    # Check for digit
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit"

    # Check for special character
    if not re.search(r'[!@#$%^&*()_+]', password):
        return "Password must contain at least one special character"

    return None