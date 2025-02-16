from fastapi import APIRouter
from src.api import user
from src.api import follow

api_router = APIRouter()
api_router.include_router(user.api, prefix="/user", tags=["user"])
api_router.include_router(follow.api, prefix="/follow", tags=["follow"])
