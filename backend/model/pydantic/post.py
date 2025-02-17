from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Post(BaseModel):
    id: int
    user_id: int
    text: str
    date : datetime