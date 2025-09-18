from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
import time
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Evaluatepost(BaseModel):
    title: str
    Content: str
    published: bool = True
    
while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='admin',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    
    except Exception as error:
        print("Database connection failed")
        print("Error: ",error)
        time.sleep(2)
        
my_posts = [{"title":"title of post 1","Content":"Content of post 1","id":1},
            {"title":"title of post 2","Content":"Content of post 2","id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i
        
@app.get("/")
def home():
    return{'message':"Welcome to My FastAPI"}

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return{"data":posts}

@app.post("/posts")
def create_posts(post: Evaluatepost):
    cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *",
                   (post.title,post.Content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return{"data":new_post}

@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("SELECT * FROM posts WHERE id = %s",(str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    return{"Post You Searched: ": post}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id:int,post:Evaluatepost):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                   (post.title,post.Content,post.published,str(id)))
    post = cursor.fetchone()
    conn.commit()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    return{"data":post}