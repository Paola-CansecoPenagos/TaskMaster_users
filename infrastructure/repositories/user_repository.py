from pymongo import MongoClient
from bson import ObjectId
import re

class UserRepository:
    def __init__(self, connection_string: str, db_name: str):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db['users']
    
    def find_by_username_or_email(self, username: str, email: str):
        return self.collection.find_one({"$or": [{"username": username}, {"email": email}]})
    
    def save_user(self, user_data: dict):
        self.collection.insert_one(user_data)

    def find_user(self, user_id):
        if re.match(r'^[0-9a-fA-F]{24}$', user_id):
            return self.collection.find_one({"_id": ObjectId(user_id)})
        return None