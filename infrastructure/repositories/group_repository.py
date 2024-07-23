from pymongo import MongoClient, ReturnDocument
from bson import ObjectId

class GroupRepository:
    def __init__(self, connection_string: str, db_name: str):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db['groups']

    def create_group(self, group_data: dict):
        self.collection.insert_one(group_data)

    def find_group_by_user_id(self, user_id: str):
        return self.collection.find_one({"members.user_id": user_id})

    def add_members_to_group(self, group_id: str, new_members: list):
        return self.collection.find_one_and_update(
            {"_id": ObjectId(group_id)},
            {"$push": {"members": {"$each": new_members}}},
            return_document=ReturnDocument.AFTER
        )