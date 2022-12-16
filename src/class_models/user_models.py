"""
Created 10/20 by Dylan Lawrence
#This file will hold most/all (for now) query and response models for users
"""
from datetime import date
from typing import List, Optional
from pydantic import BaseModel


# Users
class User(BaseModel):
    '''
    Base model for all users. All info a user can have is here
    '''
    user_id: int
    username: str
    display_name: str
    birthday: date
    friends: Optional[List[int]]

class CreateUser(BaseModel):
    '''
    Query to create a new user
    '''
    username: str
    display_name: str
    birthday: str
    password: str

class AddFriend(BaseModel):
    '''
    Query to add a friend to a users account.
    Takes the user adding a friend's username, and the username of their new friend
    '''
    username: str
    new_friend: str

