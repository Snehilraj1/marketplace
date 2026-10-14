from fastapi import APIRouter, status, Depends, HTTPException
from .. import schemas, database, models, oath2
from sqlalchemy.orm import Session

router = APIRouter(tags=['likes'], prefix="/likes")

@router.post("/")
# zero removes the vote and one adds it 
def like(payload: schemas.Like, db: Session = Depends(database.get_db), current_username = Depends(oath2.get_current_user)):
    post = db.query(models.likes).filter(models.items.item_id == payload.item_id)

    if not post:
        raise HTTPException(status_code=404, detail="the post is not available")
    vote_query = db.query(models.likes).filter( models.likes.item_id == payload.item_id, models.likes.username == current_username)
    found_vote = vote_query.first()

    if (payload.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="you have already voted")

        new_vote = models.likes(username = current_username, item_id  = payload.item_id)

        db.add(new_vote)
        db.commit()

        return {"details": "like given successully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=404, detail="vote not found")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"Details": "vote removed succesully"}