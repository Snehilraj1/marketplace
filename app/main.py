from fastapi import FastAPI
from .database import engine
from .routers import users, auth, items, likes
# importing files 
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(likes.router)