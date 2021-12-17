from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import middleware

from . import models
from .database import engine, get_db
from .routers import posts, users, auth, vote
from pydantic import BaseSettings
from .config import settings


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# models.Base.metadata.create_all(bind=engine)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")  # decorater
def root():  # function
    return {"message": "welcome to my api!!!!"}
