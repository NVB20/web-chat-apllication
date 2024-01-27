from pymongo import MongoClient
from flask import jsonify
import re
from mongo.get_mongo_address import get_db_ip_address

IP_ADDRESS = get_db_ip_address('mongodb-service', 'default')

connection_string = f"mongodb://{IP_ADDRESS}/"  
client = MongoClient(connection_string)

dbs = client.list_database_names()
message_db = client.room_messages

collections = message_db.list_collection_names()
print(collections)


def insert_messages_to_mongo(message, room):
    insert_collection = f"{room}_room_messages"
    collection = message_db[insert_collection]
    collection.insert_one(message).inserted_id
   

def create_collection(room_code):
    collection_name = f"{room_code}_room_messages"
    if collection_name not in message_db.list_collection_names():
        message_db.create_collection(collection_name)
    

def delete_collection(room_code):
    collection_name = f"{room_code}_room_messages"
    print("deleted room: ", room_code)
    message_db[collection_name].drop()


def retrieve_message_history(room_code):
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
