from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.models import models
from app.api.database.database import get_db
from app.utils.auth_utils import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter((models.User.email == user.email) | (models.User.username == user.username)).first():
        raise HTTPException(status_code=400, detail="Email or username already registered")
    hashed_pw = hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, password_hash=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/signin", response_model=schemas.Token)
def signin(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"} 