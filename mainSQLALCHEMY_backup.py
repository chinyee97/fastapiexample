from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.param_functions import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import false
from . import models
from . import schema
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()





while True:  # connection to database, retry every 2 seconds if fail
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='superuser', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error:", error)
        time.sleep(2)


@app.get("/")  # decorater
def root():  # function
    return {"message": "welcome to my api!!!"}


@app.get("/posts")  # get all post
def get_post(db: Session = Depends(get_db)):

    post = db.query(models.Post).all()  # select * from posts
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)  # create post
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")  # get post by id
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with: {id} was not found")

    return {"data": post}


# delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()

    # delete does not need to send anything back
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")  # update post
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_veri = post_query.first()

    if post_veri == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
