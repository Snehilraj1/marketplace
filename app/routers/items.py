from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from .. import models, schemas, oath2
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func

router = APIRouter(tags=["Item Management"], prefix="/item")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(item_data: schemas.ItemIn, db: Session = Depends(get_db), current_username: str = Depends(oath2.get_current_user)):
    item = db.query(models.items).filter(models.items.title == item_data.title, models.items.seller_username == current_username).first()
    if item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item with this title already exists for the current user")
    
    new_item = models.items(**item_data.model_dump(), seller_username=current_username)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {"message": "Item created successfully"}

@router.put("/{id}", status_code=status.HTTP_201_CREATED)
def update_item(id: int, payload: schemas.ItemUpdate, db: Session = Depends(get_db), current_username: models.User = Depends(oath2.get_current_user)):
    item = db.query(models.items).filter(models.items.item_id == id).first()

    if not item:
        raise HTTPException(status_code=404, detail="item not found")

    if (item.seller_username != current_username):
        raise HTTPException(status_code=403, detail="You are not authorised to update this item")

    item.price = payload.price
    item.quantity = payload.quantity

    db.commit()
    db.refresh(item)

    return item


@router.get("/my-listings")
def my_items(db: Session = Depends(get_db), current_username = Depends(oath2.get_current_user), search: Optional[str] = ""):
    items = db.query(models.items).filter(models.items.seller_username  == current_username, models.items.title.contains(search)).all()

    if not items:
        raise HTTPException(status_code=404, detail="you have no items")

    return items

# delete items
@router.delete("/{id}")
def delete_my_items(id: int, db: Session = Depends(get_db), current_username = Depends(oath2.get_current_user)):
    item = db.query(models.items).filter(models.items.item_id  == id).first()

    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    
    # check if its the user 
    if item.seller_username != current_username:
        raise HTTPException(status_code = 403, detail= "you are not authorise to delete this item")

    db.delete(item)
    db.commit()

    return {"detail": "item is deleted"}
# buy items 
@router.put("/{id}/buy", response_model= schemas.TransactionOut)
def buy_item(id: int, db: Session = Depends(get_db), current_username = Depends(oath2.get_current_user)):
    item = db.query(models.items).filter(models.items.item_id  == id).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    
    if item.seller_username == current_username:
        raise HTTPException(status_code = 403, detail= "you can not buy your own item")

    if item.quantity == 0:
        raise HTTPException(status_code=404, detail="item is out of stock")

    item.quantity -= 1

    log = models.transaction(
        buyer_username=current_username,
        item_id = item.item_id,
        title= item.title,
        price_paid=item.price,
        seller_username=item.seller_username,
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log

@router.get("/sales", response_model= list[schemas.TransactionOut] )
def my_log(db: Session = Depends(get_db), current_username = Depends(oath2.get_current_user)):
    my_log =  db.query(models.transaction).filter(models.transaction.seller_username  == current_username).all()

    if not my_log:
        raise HTTPException(status_code=404, detail="you have not sold anything yet. Be Patient :)")

    return my_log

@router.get("/history", response_model= list[schemas.TransactionOut])
def my_log(db: Session = Depends(get_db), current_username = Depends(oath2.get_current_user)):
    my_log =  db.query(models.transaction).filter(models.transaction.buyer_username  == current_username).all()

    if not my_log:
        raise HTTPException(status_code=404, detail="you have not buyed anything yet. Spend More :)")

    return my_log

@router.get("/", status_code=201, response_model=list[schemas.ItemOut])
def view_all_items(db: Session = Depends(get_db), limit: int = 5, search: Optional[str] = "" ):
    results = (
        db.query(models.items, func.count(models.likes.item_id).label("votes"))
        .join(models.likes, models.likes.item_id == models.items.item_id, isouter=True)
        .group_by(models.items.item_id)
        .filter(
            models.items.quantity > 0,
            models.items.title.contains(search)
        )
        .limit(limit)
        .all()
    )


    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no item found")

    return [
        {
            "item_id": item.item_id,
            "title": item.title,
            "quantity": item.quantity,
            "price": item.price,
            "seller_username": item.seller_username,
            "created_at": item.created_at,
            "votes": votes
        }
        for item, votes in results
    ]


@router.get("/{id}", response_model=schemas.ItemOut)
def view_item(id: int, db: Session = Depends(get_db)):
    result = db.query(models.items, func.count(models.likes.item_id).label("votes")).join(models.likes, models.likes.item_id == models.items.item_id, isouter=True).group_by(models.items.item_id).filter(models.items.item_id  == id).first()

    

    if not result:
        raise HTTPException(status_code=404, detail="item not found")

    item, votes = result

    return {
                "item_id": item.item_id,
                "title": item.title,
                "quantity": item.quantity,
                "price": item.price,
                "seller_username": item.seller_username,
                "created_at": item.created_at,
                "votes": votes
            }
        

