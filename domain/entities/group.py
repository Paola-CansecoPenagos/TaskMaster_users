from pydantic import BaseModel, Field
from typing import List, Dict
from bson import ObjectId

class Group(BaseModel):
    members: List[Dict[str, str]]  # Cambia dict a un diccionario tipado
