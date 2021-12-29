from typing import Optional, List
from fastapi import FastAPI, Response,status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random  import randrange
import psycopg2
from  psycopg2.extras import RealDictCursor
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND 
import time

from . import  schemas

from fastapi import Depends
from sqlalchemy.orm import Session
from . import  models
from .database import  engine,get_db

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



@app.get("/")
async def root():
    return {"message": "WElcome to my World"}


@app.get("/posts",response_model=List[schemas.Post])
def get_post( db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts =cursor.fetchall()
    posts= db.query(models.Post).all()
    return posts


@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title,  content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post= cursor.fetchone()
    # conn.commit()

    # new_post= models.Post(title=post.title, content= post.content,published= post.published)
    new_post= models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id:int, response: Response ,db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post =cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == str(id)).first()
    if not post:
          raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f" post with id:{id} was not found")
    return  post


# deleteing a post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
    # deleted_post =cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == str(id))
    post =post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, 
                            detail= f" post with id:{id} was not found")
    post_query.delete(synchronize_session=False)
    db.commit()
    return  Response( status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title= %s,  content=%s,published=%s  WHERE id = %s RETURNING * """,(post.title,post.content,post.published, str(id)))
    # updated_post =cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == str(id))
    updated_post =post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, 
                            detail= f" post with id:{id} was not found")
    # post_query.update({"title":"this is updated title", "content": "this is updated content"},synchronize_session=False)
    post_query.update(post.dict(),synchronize_session=False)

    db.commit()

    return post_query.first()