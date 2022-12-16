"""
root file for gift tracker api
will pull together end points and models
"""
import os
from typing import List
import psycopg2
import uvicorn
import sqlalchemy
from fastapi.middleware.cors import CORSMiddleware
from request_functions import event_requests, user_requests
from fastapi import FastAPI

from dotenv import load_dotenv

#custom modules
from db_utils.sql_utils import make_simple_query
from db_utils.metadata import users, events, credentials
from class_models import user_models, event_models


#append folder paths

#load in db connection string
load_dotenv()


#create engine

engine = sqlalchemy.create_engine(os.environ['DB_URL'])


app = FastAPI()

# cors setup
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()


@app.get("/")
def read_root():
    """
    does nothing..... yet
    """
    return {"Hello": "World"}

@app.get("/getallusers", response_model = List[user_models.User])
def get_all_users():
    """
    Temporary helper end point to retrieve all users
    """
    select = users.select()

    result = make_simple_query(select, engine).fetchall()

    return result

@app.get("/getuser/{username}/{password}", response_model = user_models.User)
def read_item(username: str, password: str):
    """
    Gets a user from the db that matches the username
    """
    #set username to lower
    username = username.lower()
    #create select statement
    select = users.select().where(users.c.username == username)
    #get result, fetch first item
    result = make_simple_query(select, engine).fetchone()

    if result is None:
        print("Error fetching user")
        return 500

    #now check for pw
    select = credentials.select().where(credentials.c.user_id == result.user_id)
    try:
        correct_password = make_simple_query(select, engine).fetchone()
        print(correct_password)
        if correct_password.password != password:
            print("Incorrect password")
            return 500
    except:
        print("Error fetching password")
        return 500


    return result

@app.post("/createuser")
def create_user(user: user_models.CreateUser):
    """
    Creates a new user and adds them to the DB
    """
    #set username to lower
    user.username = user.username.lower()
    #insert statement to create new user
    insert = users.insert().values(username = user.username,
                                   display_name = user.display_name,
                                   birthday = user.birthday)
    #make query
    try:
        make_simple_query(insert, engine)
        #get new user user id 

        #create new event for users birthday
        new_user_query = users.select(users.c.username == user.username)
        print(user.username)
        new_user: user_models.User = make_simple_query(new_user_query, engine).fetchone()
        print(new_user)
        insert_query = events.insert().values(
            event_for = new_user.user_id,
            event_name = f'{new_user.display_name}\'s Birthday',
            event_description = f'Automatically generated birthday event for {new_user.display_name}',
            event_date = new_user.birthday
        )
        make_simple_query(insert_query, engine)
    except psycopg2.Error:
        print("Exception encountered at /createuser")
        return 500

    #now add password
    insert_password = credentials.insert().values(
        user_id = new_user.user_id,
        password = user.password
    )
    try:
        make_simple_query(insert_password, engine)

    except Exception as e:
        print(e)
        print("Exception encountered at /createuser")
        return 500

    return new_user

@app.post("/addfriend")
def add_friend_endpoint(req: user_models.AddFriend):
    '''
    Calls the function to add a friend
    '''
    return user_requests.add_friend(req, engine)

@app.get('/getevents/{users_list}')#, response_model=List[event_models.Event])
def get_events_endpoint(users_list: str):
    """
    endpoint to get events
    """
    return event_requests.get_events(users_list, engine)

@app.post('/addevent')
def add_event_endpoint(req: event_models.Event):
    """
    endpoint to add event to database
    """
    return event_requests.add_event(req, engine)

@app.post('/idea/{user}/{event_for}/{gift_name}')
def add_idea(user: int, event_for: int, gift_name: str):
    print(gift_name)
    return event_requests.add_idea(user, event_for, gift_name, engine)

@app.get('/idea/{user}/{event_for}')
def get_ideas(user: int, event_for: int):
    return event_requests.get_idea(user, event_for, engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
