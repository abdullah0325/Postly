from fastapi import APIRouter
from app.api.endpoints import auth, posts, comments, likes,chat

router = APIRouter()
# Routers for social media app will be included here

router.include_router(auth.router, tags=["Auth"])
router.include_router(posts.router, tags=["Posts"])
router.include_router(chat.router, tags=["Chat"])
router.include_router(comments.router, tags=["Comments"])
router.include_router(likes.router, tags=["Likes"])
