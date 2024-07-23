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
        result = self.collection.insert_one(user_data)
        return result
    
    def find_user(self, user_id):
        if re.match(r'^[0-9a-fA-F]{24}$', user_id):
            return self.collection.find_one({"_id": ObjectId(user_id)})
        return None
    
    def find_by_token(self, token):
        return self.collection.find_one({"confirmation_token": token})

    def confirm_user(self, user_id):
        self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"confirmed": True}})
    
    def get_all_usernames_except(self, user_id: str):
        pipeline = [
            {"$match": {"_id": {"$ne": ObjectId(user_id)}}},
            {"$project": {"username": 1, "_id": 0}}
        ]
        return list(self.collection.aggregate(pipeline))