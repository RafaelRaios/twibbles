from typing import Optional
from pydantic import BaseModel
from model.pydantic.user import User


class Following(BaseModel):
    follower_id: int
    followed_id: int

    follower: Optional[User]
    followed: Optional[User]
