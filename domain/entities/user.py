from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
