#Created 10/20 by Dylan Lawrence
#This file will hold most/all (for now) query and response models for users
from typing import List, Optional
from pydantic import BaseModel


# Users
class User(BaseModel):
    user_id: int
    username: str
    display_name: str
    birthday: str
    friends: Optional[List[int]]
    
class CreateUser(BaseModel):
    username: str
    display_name: str
    birthday: str