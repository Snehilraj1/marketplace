from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, oath2
from ..database import get_db
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["Authentication"]) 

@router.post("/login", status_code=status.HTTP_201_CREATED)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    if not user_data:
        raise HTTPException(status_code = 404, detail = f"User with username {user_credentials.username} not found")

    attempted_password = user_credentials.password
    hashed_password = user_data.password
    if not pwd_context.verify(attempted_password, hashed_password):
        raise HTTPException(status_code = 404, detail = f"Incorrect password for user {user_credentials.username}")
    

    token_id = oath2.create_access_token(data={"username": user_data.username})
    return {"access_token": token_id, "token_type": "bearer"}
    

    

    

    