from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from templates import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from utils import hash_password
import models
from database import engine, Local_session, get_db

from time import localtime

from router import user_api, post_api, auth




models.Base.metadata.create_all(bind=engine)
hours, minutes, seconds = localtime()[3:6]

print(f'New connection has been established. The time is {hours}:{minutes}:{seconds}')

app = FastAPI()

app.include_router(post_api.router)
app.include_router(user_api.router)
app.include_router(auth.router)
#%%


