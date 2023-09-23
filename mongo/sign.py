from flask import request
from pymongo import MongoClient
from mongo.get_mongo_address import get_db_ip_address
import bcrypt


#IP_ADDRESS = get_db_ip_address('mongodb-service', 'default')

connection_string = f"mongodb://172.17.0.2/"  
client = MongoClient(connection_string)
users_db = client.users

def check_user_exists(email):
    existing_user = users_db["users"].find_one({"email": email})
    return existing_user is not None


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def new_user(user_data):
    users_db["users"].insert_one(user_data)
    return "User added successfully"

def login_user():
    email = request.form.get("email")
    password = request.form.get("password")

    user_data = users_db["users"].find_one({"email": email})

    if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data["password"]):
        return True
    else:
        return False

def register_user():
    email = request.form.get("email")
    password = request.form.get("password")

    hashed_password = hash_password(password)

    data = {
        "email": email,
        "password": hashed_password
    }

    new_user(data)
    return "User registered successfully"