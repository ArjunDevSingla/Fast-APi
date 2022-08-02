import string
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, status, Response
from random import randrange
from pydantic import BaseModel
import psycopg2
# from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi1',user='postgres',password='161202')
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Connecting to Database failed")
        print("Error: ", error)
        time.sleep(5)


# def find_post(id):
#     for p in my_array:
#         if p['id'] == id:
#             return p

# def delete_post(id):
#     for i, p in enumerate(my_array):
#         if p['id'] == id:
#             my_array.pop(i)
#             return i
            

# def find_index_post(id):
#     for i, p in enumerate(my_array):
#         if p['id'] == id:
#             return i


@app.get("/")
def root():
    return {"message": "Welcome to the Application"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"Post" : posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchall()
    conn.commit()
    return {"posts": new_post}


@app.get("/posts/{id}")
def retrieve_post(id: str):
    cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    # print(post)
    # post = findpost(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail= f"The post with id: {id} is not found")
    return {"One post": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: str):
    cursor.execute(f"""DELETE FROM posts WHERE id = {id} RETURNING *""")
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The post with id = {id} is not available")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}")
# def update_posts(id: int, post: post):
#     index = find_index_post(id)

#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_array[index] = post_dict
#     return {"data": post_dict}