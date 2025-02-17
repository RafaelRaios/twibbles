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

<<<<<<< Updated upstream
        if user is None:
            return None
        return {"status": "ok", "data": user}
=======
            user = UserPydantic(id=user.id,
                                user_name=user.user_name,
                                email=user.email,
                                is_private=user.is_private,
                                profile_img_path=user.profile_img_path,
                                bio=user.bio,
                                ).model_dump()

            return HttpResponseModel(status_code=200,
                                     message="User found",
                                     data=user)
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))

def get_users_by_substring(substring: str):
    try:
        with Session(postgresql_engine) as session:
            statement = select(User).where(User.user_name.contains(substring))
            users = session.execute(statement).scalars().all()

            users = [UserPydantic(id=user.id,
                                  user_name=user.user_name,
                                  profile_img_path=user.profile_img_path,
                                  ).model_dump() for user in users]

            return HttpResponseModel(status_code=200,
                                     message="Users found",
                                     data=users)
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))
    
def update_user_privacy(user_id: int, is_private: bool):
    try:
        with Session(postgresql_engine) as session:
            statement = select(User).where(User.id == user_id).limit(1)
            user = session.execute(statement).scalars().first()

            if user is None:
                return HttpResponseModel(status_code=404, message="User not found")
            
            user.is_private = is_private
            session.commit()

            return HttpResponseModel(status_code=200,
                                        message="User privacy updated")
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))
    
>>>>>>> Stashed changes
