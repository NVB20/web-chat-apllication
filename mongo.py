from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from flask import jsonify
import re

 
load_dotenv(find_dotenv())

#password = os.environ.get("MONGODB_PWD")

connection_string = "mongodb://127.0.0.1:27017/"  

client = MongoClient(connection_string)

dbs = client.list_database_names()
message_db = client.messages

collections = message_db.list_collection_names()
print(collections)



def insert_messages_to_mongo(message, room):
    insert_collection = f"{room}_room_messages"
    collection = message_db[insert_collection]
    test_message = message
    inserted_id = collection.insert_one(test_message).inserted_id
    print(inserted_id)


def create_collection(room_code):
    collection_name = f"{room_code}_room_messages"
    message_db.create_collection(collection_name)
    

def delete_collection(room_code):
    collection_name = f"{room_code}_room_messages"
    print("deleted room: ", room_code)
    message_db[collection_name].drop()


def retrive_message_history(room_code):
    collection_name = f"{room_code}_room_messages"
    cursor = message_db[collection_name].find()
    
    message_list = []
    
    for document in cursor:
        name = document['name']
        content = document['message']
        timestamp = document['time']
        
        pattern = '(\d{2}:\d{2})'
        time = re.match(pattern, timestamp).group(1)
        
        message_list.append((name, content, time))      
    
    return jsonify(message_list)
