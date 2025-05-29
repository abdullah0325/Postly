from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas
from app.models import models
from app.api.database.database import get_db
from app.utils.auth_utils import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/posts", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_post = models.Post(**post.dict(), user_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/posts", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

@router.get("/posts/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.get("/me/posts", response_model=List[schemas.PostOut])
def get_my_posts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Post).filter(models.Post.user_id == current_user.id).all()

@router.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id, models.Post.user_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"} 