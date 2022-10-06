from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class User(BaseModel):
    name: str
    birthday: str
    friends: List[str]

app = FastAPI()




@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/getuser/{userid}", response_model = User)
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}