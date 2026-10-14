from pydantic import BaseModel, ConfigDict, Field, computed_field, EmailStr
from typing import Annotated, Literal, Optional
from datetime import datetime

class UserIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: Annotated[str, Field(description="The username of the user", min_length=3)]
    email: Annotated[EmailStr, Field(description="The email of the user")]
    password: Annotated[str, Field(description="The password of the user", min_length=6)]

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    created_at: datetime

class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: Optional[Annotated[str, Field(description="The new username of the user", min_length=3)]] = None
    email: Optional[Annotated[EmailStr, Field(description="The new email of the user")]] = None
    password: Optional[Annotated[str, Field(description="The new password of the user", min_length=6)]] = None

class ItemIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: Annotated[str, Field(description="The title of the item", min_length=1)]
    price: Annotated[float, Field(description="The price of the item", gt=0)]
    quantity: Annotated[int, Field(description="The quantity of the item", gt=0)] = 1

class ItemUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    price: Annotated[float, Field(description="The price of the item", gt=0)]
    quantity: Annotated[int, Field(description="The quantity of the item", gt=0)] = 1

class Transaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    price_paid: Annotated[float, Field(description="The price of the item", gt=0)]
    item_id : int
    seller_username : str
    buyer_username : str

class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transaction_id : int
    item_id: int
    title : str
    seller_username : str
    buyer_username : str
    price_paid: Annotated[float, Field(description="The price of the item", gt=0)]
    purchased_at: datetime

class Like(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    item_id: int 
    dir: Literal[0, 1] 

class ItemOut(BaseModel):
    item_id: int
    title: str
    quantity: int
    price: int 
    seller_username: str
    created_at: datetime
    votes: int

    model_config = ConfigDict(from_attributes=True)


    