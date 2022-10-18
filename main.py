from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


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
    name: str
    birthday: str
    friends: List[str]

app = FastAPI()




@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/getuser/{userid}", response_model = User)
def read_item(item_id: int, q: Union[str, None] = None):
    return {"user": "test"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)