from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, oath2
from ..database import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags=["User Management"], prefix="/user")

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(payload: schemas.UserIn, db: Session = Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.username == payload.username).first()
    if user_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    hashed_password = pwd_context.hash(payload.password)
    new_user = models.User(username=payload.username, email=payload.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/search/{username}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(username: str, db: Session = Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.username == username).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_data

@router.get(
    "/me", status_code=status.HTTP_200_OK, response_model=schemas.UserOut
)
def get_my_profile(
    db: Session = Depends(get_db),
    current_username: str = Depends(oath2.get_current_user),
):
  user_data = (
      db.query(models.User)
      .filter(models.User.username == current_username)
      .first()
  )

  if not user_data:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )

  return user_data

@router.put("/me", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def update_my_profile(
    payload: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_username: str = Depends(oath2.get_current_user),
):
    user_data = (
        db.query(models.User)
        .filter(models.User.username == current_username)
        .first()
    )

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found" 
        )

    if payload.username:
        user_data.username = payload.username
    if payload.email:
        user_data.email = payload.email
    if payload.password:
        hashed_password = pwd_context.hash(payload.password)
        user_data.password = hashed_password

    db.commit()
    db.refresh(user_data)

    return user_data

@router.delete("/me", response_model=schemas.UserOut)
def self_destruct(
    db: Session = Depends(get_db),
    current_username: str = Depends(oath2.get_current_user)
    ):
    user_data = db.query(models.User).filter(models.User.username == current_username)
    user = user_data.first()
        

    user_data.delete()
    db.commit()

    return user



