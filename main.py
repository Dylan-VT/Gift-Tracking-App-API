"""
root file for gift tracker api
will pull together end points and models
"""
import os
import psycopg2
import uvicorn
import sqlalchemy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

#custom modules
from metadata import users
from models import user_models



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

    #first verify friend is exists
    select = users.select().where(
                            users.c.username == req.new_friend)

    new_friend_result = make_simple_query(select, engine).fetchone()

    #return 201 if no friend
    if new_friend_result is None:
        print("Couldn't find new friend")
        return 201

    #now update
    update = users.c.friends.append(new_friend_result.user_id)  # type: ignore

    result = make_simple_query(update, engine)

    print(result)


    return 400

def make_simple_query(sql_statement, _e):
    """
    simple function that takes a sql statement and engine and returns the result of the query
    """
    #open connection
    with _e.connect() as conn:
        #make query
        result = conn.execute(sql_statement)
        return result



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
