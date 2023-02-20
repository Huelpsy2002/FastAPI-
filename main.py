
from asyncio.windows_events import NULL

import time
import http
from pickle import TRUE
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(host='hostname', database='db name',
                                user='username', cursor_factory=RealDictCursor, password='password')
        cursor = conn.cursor()
        print("database connection succesfull!")
        break
    except Exception as erro:

        print("connecting to database was failed")
        print(f"Error: {erro}")
        time.sleep(2)




@app.get("/")
def root():

    return {"message": "Hello "}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM post """)
    post = cursor.fetchall()

    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createpost(post: Post):
    cursor.execute(
        """INSERT INTO  post (title , content , published) VALUES (%s , %s  ,%s) RETURNING *  """,
        (post.title, post.content, post.published))
    new_post = cursor.fetchone()     
    conn.commit()
    return new_post


@app.get("/posts/latest")
def get_latest_post():
    cursor.execute(""" select * from post order by id desc limit 1 """)
    post = cursor.fetchone()
                     

    return post


@app.get("/posts/{id}")
def get_post(id: int, response: Response):              
    cursor.execute("""SELECT * FROM post WHERE id = %s  """ , (str(id),))
    post = cursor.fetchone()

    
    if not post:
       

        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=  
                            f'post was not found')

    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id):
    cursor.execute(""" DELETE FROM post WHERE id = %s RETURNING * """ , (str(id),))
    post =  cursor.fetchone()
    conn.commit()
   
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} does not exist')

   

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE post SET title = %s ,content = %s , published = %s WHERE id = %s  RETURNING *""" , (post.title ,
    post.content , post.published  , str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    
   

    if updated_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} does not exist')

   

    return updated_post


