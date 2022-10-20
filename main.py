from cgitb import reset
from typing import Union
from unittest import result
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from models import user_models
from metadata import users
import sqlalchemy


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
    return {"Hello": "World"}


@app.get("/getuser/{username}")
def read_item(username: str, q: Union[str, None] = None):
    #create select statement
    select = users.select().where(users.c.username == username)
    #get result, fetch first item
    result = make_simple_query(select, engine).fetchone()
    if result is None:
        print("Error fetching user")
        return 500
    
    return result
    
@app.post("/createuser")
def create_item(user: user_models.CreateUser):
    #insert statement to create new user
    insert = users.insert().values(username = user.username, display_name = user.display_name, birthday = user.birthday)
    #make query
    try:
        result = make_simple_query(insert, engine)
    except:
        print("Exception encountered at /createuser")
        return 500
    
    return 200


#simple function that takes a sql statement and engine and returns the result of the query
def make_simple_query(sql_statement, engine):
    #open connection
    with engine.connect() as conn:
        #make query
        result = conn.execute(sql_statement)
        return result

        

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)