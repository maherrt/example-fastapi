from typing import Optional
from fastapi import FastAPI, Response,status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from random  import randrange
import psycopg2
from  psycopg2.extras import RealDictCursor
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND 
import time


app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published: bool = True
    rating: Optional[int]=None

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



my_posts =[{"title":"title of post 1","content":" content of post 1", "id":1},
           {"title":"title of post 2","content":" content of post 2", "id":2}]

@app.get("/")
async def root():
    return {"message": "WElcome to my World"}


@app.get("/posts")
def get_post():
    cursor.execute(""" SELECT * FROM posts """)
    posts =cursor.fetchall()
    # print(posts)
    return {"data": posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    
    cursor.execute(""" INSERT INTO posts (title,  content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    new_post= cursor.fetchone()
    conn.commit()

    return {"data":  new_post}

# def find_post(id):
#     return [post for post in my_posts if post["id"] == int(id)]


@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""",(str(id),))
    post =cursor.fetchone()
    if not post:
          raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f" post with id:{id} was not found")
    return {"post_details": post}


# deleteing a post
# def find_post(id: int):
#     # return my_posts.index(id)
#     return next((index for (index, post) in enumerate(my_posts) if post["id"] == id), None)

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
    deleted_post =cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, 
                            detail= f" post with id:{id} was not found")

    return  Response( status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute(""" UPDATE posts SET title= %s,  content=%s,published=%s  WHERE id = %s RETURNING * """,(post.title,post.content,post.published, str(id)))
    updated_post =cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, 
                            detail= f" post with id:{id} was not found")
    
    return { 'data': updated_post}