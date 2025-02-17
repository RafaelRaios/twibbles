from src.engine import postgresql_engine
from sqlalchemy.orm import Session
from model.sqlalchemy.user import User
from model.sqlalchemy.post import Post
from model.sqlalchemy.following import Following
from model.sqlalchemy.follow_requests import FollowRequest
from model.pydantic.user import Post as PostPydantic

from src.schemas.response import HttpResponseModel

from datetime import dt

from sqlalchemy import select

    
def post_post(user_id: int, text: str):
    try:
        with Session(postgresql_engine) as session:
            post = PostPydantic(user_id=user_id, text=text, date=dt.strftime("%Y-%m-%d %H:%M:%S"))
            session.add(post)
            session.commit()
            return HttpResponseModel(status_code=200,
                                     message="Post created",)
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))
    