from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas
from app.models import models
from app.api.database.database import get_db
from app.api.endpoints.posts import get_current_user

router = APIRouter()

@router.post("/posts/{id}/comment", response_model=schemas.CommentOut)
def add_comment(id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db_comment = models.Comment(text=comment.text, user_id=current_user.id, post_id=id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/posts/{id}/comments", response_model=List[schemas.CommentOut])
def get_comments(id: int, db: Session = Depends(get_db)):
    return db.query(models.Comment).filter(models.Comment.post_id == id).all()

@router.delete("/comment/{id}")
def delete_comment(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == id, models.Comment.user_id == current_user.id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted"} 