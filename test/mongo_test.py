import unittest
from unittest import mock
from pymongo import MongoClient
from mongomock import MongoClient as MockMongoClient

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from mongo import insert_messages_to_mongo, delete_collection

class TestMongoFunctions(unittest.TestCase):
    @mock.patch('pymongo.MongoClient', MockMongoClient)
    def setUp(self):
        self.client = MongoClient() 
        self.message_db = self.client.messages

    def tearDown(self):
            self.client.drop_database('messages')
    
    def test_insert_messages_to_mongo(self):
        message = {
            'name': 'user1',
            'message': 'Hello, world!',
            'time': '12:34'
        }
        room = 'test_room'

        insert_messages_to_mongo(message, room)

        collection = self.message_db[f"{room}_room_messages"]
        self.assertEqual(collection.count_documents({}), 1)     
        
    def test_delete_collection(self):
        room_code = 'test_room'
        collection_name = f"{room_code}_room_messages"

        self.message_db.create_collection(collection_name)
        self.assertEqual(self.message_db.list_collection_names(), [collection_name])

        delete_collection(room_code)
        self.assertEqual(self.message_db.list_collection_names(), [])   
        
        
if __name__ == '__main__':  
    unittest.main()
