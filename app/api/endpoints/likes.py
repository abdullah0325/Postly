from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas
from app.models import models
from app.api.database.database import get_db
from app.api.endpoints.posts import get_current_user

router = APIRouter()

@router.post("/posts/{id}/like", response_model=schemas.LikeOut)
def like_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    existing_like = db.query(models.Like).filter(models.Like.user_id == current_user.id, models.Like.post_id == id).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked")
    db_like = models.Like(user_id=current_user.id, post_id=id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

@router.get("/posts/{id}/likes", response_model=List[schemas.LikeOut])
def get_likes(id: int, db: Session = Depends(get_db)):
    return db.query(models.Like).filter(models.Like.post_id == id).all()

@router.delete("/like/{id}")
def unlike(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    like = db.query(models.Like).filter(models.Like.id == id, models.Like.user_id == current_user.id).first()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found or not authorized")
    db.delete(like)
    db.commit()
    return {"detail": "Like removed"} 