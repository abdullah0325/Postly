# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.api.database.database import get_db
# from app.utils.auth_utils import decode_access_token
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from app.schemas import schemas
# from app.models import models

# router = APIRouter()
# security = HTTPBearer()

# def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
#     token = credentials.credentials
#     user_id = decode_access_token(token)
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")
#     return user

# @router.post("/chat/send", response_model=schemas.MessageOut)
# def send_message(message: schemas.MessageCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
#     new_msg = models.Message(
#         content=message.content,
#         sender_id=current_user.id,
#         receiver_id=message.receiver_id
#     )
#     db.add(new_msg)
#     db.commit()
#     db.refresh(new_msg)
#     return new_msg

# @router.get("/chat/{other_user_id}", response_model=list[schemas.MessageOut])
# def get_messages(other_user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
#     messages = db.query(models.Message).filter(
#         ((models.Message.sender_id == current_user.id) & (models.Message.receiver_id == other_user_id)) |
#         ((models.Message.sender_id == other_user_id) & (models.Message.receiver_id == current_user.id))
#     ).order_by(models.Message.timestamp).all()
#     return messages


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.database.database import get_db
from app.utils.auth_utils import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas import schemas
from app.models import models

router = APIRouter()
security = HTTPBearer()

# Helper to get current user from token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# ✅ Get All Users (except current user)
@router.get("/users", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    users = db.query(models.User).filter(models.User.id != current_user.id).all()
    return users

# ✅ Send a message
@router.post("/chat/send", response_model=schemas.MessageOut)
def send_message(message: schemas.MessageCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_msg = models.Message(
        content=message.content,
        sender_id=current_user.id,
        receiver_id=message.receiver_id
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

# ✅ Get messages between current user and other user
@router.get("/chat/{other_user_id}", response_model=list[schemas.MessageOut])
def get_messages(other_user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    messages = db.query(models.Message).filter(
        ((models.Message.sender_id == current_user.id) & (models.Message.receiver_id == other_user_id)) |
        ((models.Message.sender_id == other_user_id) & (models.Message.receiver_id == current_user.id))
    ).order_by(models.Message.timestamp).all()
    return messages



@router.get("/me", response_model=schemas.UserOut)
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    return current_user