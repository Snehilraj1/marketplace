from fastapi import FastAPI
from .database import engine
from .routers import users, auth, items, likes
# importing files 
from . import models
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

# origins = ['https://www.google.com']

app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(likes.router)


@app.get("/")
def guide():
    return {"message": "open the docs"}

