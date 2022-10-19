import dis
from typing import Optional, Union
from click import echo
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import sqlalchemy
#load in db connection string
load_dotenv()


#create engine

engine = sqlalchemy.create_engine(os.environ['DB_URL'], echo = True)


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


class User(BaseModel):
    user_id: int
    username: str
    display_name: str
    birthday: str
    friends: Optional[List[str]]

app = FastAPI()




@app.get("/")
def read_root():
    #connect to db
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text('SELECT * FROM public.users;'))
        for r in result:
            print(r)   
    return {"Hi": "Bye"}


@app.get("/getuser/{username}")
def read_item(username: str, q: Union[str, None] = None):
    #connect to db
    with engine.connect() as conn:
        #execute query
        result = conn.execute(sqlalchemy.text(f'SELECT username, user_id, display_name, birthday, friends FROM public.users WHERE "username" = \'{username}\';'))
        r = result.fetchone()
        
        #verify r exists
        if not r:
            return 501
        
        found_user = User(user_id = r[1], username = r[0], display_name = r[2], birthday = str(r[3]), friends = r[4])
        
        return found_user
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)