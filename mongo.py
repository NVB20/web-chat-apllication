from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import os
from room_manager import rooms
import pprint


load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")
 
connection_string = f"mongodb+srv://nivb49:{password}@messages-cluster.rhcbhja.mongodb.net/"
client = MongoClient(connection_string)

dbs = client.list_database_names()
message_db = client.messages

collections = message_db.list_collection_names()
print(collections)



def insert_messages(message, room):
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
