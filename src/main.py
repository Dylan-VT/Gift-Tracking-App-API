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
from request_functions.event_requests import get_events, add_event

from fastapi import FastAPI

from dotenv import load_dotenv

#custom modules
from db_utils.sql_utils import make_simple_query
from db_utils.metadata import users
from models import user_models, event_models



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

@app.get("/getuser/{username}", response_model = user_models.User)
def read_item(username: str):
    """
    Gets a user from the db that matches the username
    """
    #create select statement
    select = users.select().where(users.c.username == username)
    #get result, fetch first item
    result = make_simple_query(select, engine).fetchone()

    if result is None:
        print("Error fetching user")
        return 500

    return result

@app.post("/createuser")
def create_user(user: user_models.CreateUser):
    """
    Creates a new user and adds them to the DB
    """
    #insert statement to create new user
    insert = users.insert().values(username = user.username,
                                   display_name = user.display_name,
                                   birthday = user.birthday)
    #make query
    try:
        make_simple_query(insert, engine)
    except psycopg2.Error:
        print("Exception encountered at /createuser")
        return 500

    return 200

@app.post("/addfriend")
def add_friend(req: user_models.AddFriend):
    '''
    query to create a new friend, takes the username of the original friend
    and the new friend to add
    '''
    #users cannot add themselves as friends
    if req.username == req.new_friend:
        return 501

    #first verify friend is exists
    select = users.select().where(
                            users.c.username == req.new_friend)

    new_friend_result = make_simple_query(select, engine).fetchone()

    #return 201 if no friend
    if new_friend_result is None:
        print("Couldn't find new friend")
        return 502

    #get original users friends
    select = users.select().where(
                            users.c.username == req.username
    )

    original_user = make_simple_query(select, engine).fetchone()

    #if no friends found or friend in list return a 5xx

    if original_user is None:
        return 503

    original_user_friends = original_user.friends  # type: ignore
    #instantiate list of friends if empty
    if original_user_friends is None:
        original_user_friends = []

    if req.new_friend in original_user_friends:
        return 504

    #update original users friends
    original_user_friends.append(new_friend_result.user_id)  # type: ignore
    print(original_user_friends)

    #now update in db

    update = users.update().where(
        users.c.username == req.username
    ).values(
        {"friends": original_user_friends}
    )


    make_simple_query(update, engine)

    return 400

@app.get('/getevents/{users_list}', response_model=List[event_models.Event])
def get_events_endpoint(users_list: str):
    """
    endpoint to get events
    """
    return get_events(users_list, engine)

@app.post('/addevent')
def add_event_endpoint(req: event_models.Event):
    """
    endpoint to add event to database
    """
    return add_event(req, engine)






if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
