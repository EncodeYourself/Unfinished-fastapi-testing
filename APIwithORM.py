from fastapi import FastAPI
import models
from database import engine
from time import localtime
from router import user_api, post_api, auth, likes




models.Base.metadata.create_all(bind=engine)
hours, minutes, seconds = localtime()[3:6]

print(f'New connection has been established. The time is {hours}:{minutes}:{seconds}')

app = FastAPI()

app.include_router(post_api.router)
app.include_router(user_api.router)
app.include_router(auth.router)
app.include_router(likes.router)
#%%


