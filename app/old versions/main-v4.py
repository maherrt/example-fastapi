from fastapi import FastAPI,Depends
from fastapi.param_functions import Body
from sqlalchemy.orm import Session

import psycopg2
from  psycopg2.extras import RealDictCursor

from random  import randrange
import time

from . import  models , schemas, utils
from .database import  engine,get_db
from .routers  import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn= psycopg2.connect(host='localhost' ,database='fastapi', user='postgres', password='maramsen', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print(" database connection was succussfull")
        break
    except Exception as error:
        print(" database connectionfailed")
        print('Error: ',error)
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

