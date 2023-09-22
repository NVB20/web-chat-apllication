from flask import request, jsonify
from pymongo import MongoClient
from mongo.get_mongo_address import get_db_ip_address
import bcrypt


IP_ADDRESS = get_db_ip_address('mongodb-service', 'default')

connection_string = f"mongodb://{IP_ADDRESS}/"  
client = MongoClient(connection_string)
users_db = client.users


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def user_login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = users_db["users"].find_one({"email": email})
    if user and check_password(password, user['password']):
        return True
    return False


def new_user(user_data):
    users_db["users"].insert_one(user_data)
    return "User added successfully"


def register_user():
    email = request.form.get("email")
    password = request.form.get("password")

    hashed_password = hash_password(password)  

    data = {
        "email": email,
        "password": hashed_password
    }
    new_user(data)

