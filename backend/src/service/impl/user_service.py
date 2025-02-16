from src.engine import postgresql_engine
from sqlalchemy.orm import Session
from model.sqlalchemy.user import User
from model.sqlalchemy.following import Following
from model.sqlalchemy.follow_requests import FollowRequest
from model.pydantic.user import User as UserPydantic

from sqlalchemy import select


def get_user(user_id: int):
    with Session(postgresql_engine) as session:
        statement = select(User).where(User.id == user_id).limit(1)
        user = session.execute(statement).scalars().first()

        user = UserPydantic(id=user.id,
                            user_name=user.user_name,
                            email=user.email,
                            is_private=user.is_private)

        if user is None:
            return None
        return {"status": "ok", "data": user}