from sqlalchemy import Column, Float, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql import func
from .database import Base
from pydantic import EmailStr

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)


class items(Base):
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)
    seller_username = Column(String, ForeignKey("users.username", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)


class transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, index=True)
    title = Column(String, nullable=False)
    seller_username = Column(String, nullable=False)
    buyer_username = Column(String, nullable=False)
    price_paid = Column(Float, nullable=False)
    purchased_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

class likes(Base):
    __tablename__ = "likes"

    username = Column(String, ForeignKey("users.username", ondelete="CASCADE"), primary_key=True)
    item_id = Column(Integer,ForeignKey("items.item_id", ondelete="CASCADE"), primary_key=True)

