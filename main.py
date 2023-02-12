
from asyncio.windows_events import NULL
import http
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str




my_posts = [{"title": "post1", "content": "content of post1", "id": 1}, {
    "title": "post2", "content": "content of post2", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
def find_index(id):
    for i ,p in enumerate(my_posts):
        if p['id']==id:
            return i
       
    

@app.get("/")
def root():

    return {"message": "Hello "}


@app.get("/posts")
def get_posts():                                         # get all posts
    return {"data": my_posts}


@app.post("/posts",status_code= status.HTTP_201_CREATED)
def createpost(post: Post):
    post_dict = post.dict()                              # create a post
    post_dict['id'] = randrange(0, 1000)
    my_posts.append(post_dict)
    
    return post_dict


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]                     # get latest post

    return post


@app.get("/posts/{id}")
def get_post(id: int, response: Response):               # get a  post
                                                       
    post = find_post(int(id))
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND          //method 1
        # return {'message':'post was not found'}           

        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=   #//method 2
                            f'post was not found')

    return {"post_detail": post}



@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id):
    post = find_post(int(id))                                        #delete post
    if not post:
         raise HTTPException(status.HTTP_404_NOT_FOUND, detail=  
                            f'post with id:{id} does not exist')

    my_posts.remove(post)

    return Response(status_code=status.HTTP_204_NO_CONTENT)  



@app.put("/posts/{id}")
def update_post(id:int,update_post:Post):
    index = find_index(id)
    # mypost = find_post(id)                                               #update post

    if index ==None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f'post with id:{id} does not exist')

    update_post_dict = update_post.dict()
    update_post_dict['id'] = id
    my_posts[index] = update_post_dict
   
    





    return "post updated"



