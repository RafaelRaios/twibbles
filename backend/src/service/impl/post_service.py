from src.engine import postgresql_engine
from sqlalchemy.orm import Session
from model.sqlalchemy.user import User
from model.pydantic.user import User as UserPydantic

from model.sqlalchemy.post import Post
from model.pydantic.post import Post as PostPydantic
from model.pydantic.post import CreatePost as CreatePostPydantic
from src.service.impl import follow_service

from src.schemas.response import HttpResponseModel

from sqlalchemy import select

def get_posts(user_id: int):
    try:
        with Session(postgresql_engine) as session:
            statement = select(Post, User).join(User, User.id == Post.user_id).where(Post.user_id == user_id).order_by(Post.date_time.desc())
            posts = session.execute(statement).fetchall()

            if posts is None:
                return HttpResponseModel(status_code=404, message="No posts were found")

            result = []
            for p in posts:
                p = p.Post
                post = PostPydantic(id=p.id,
                                    user_id=p.user_id,
                                    text=p.text,
                                    date_time=p.date_time).model_dump()
                result.append(post)

            return HttpResponseModel(status_code=200,
                                     message="Posts found",
                                     data=result)
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))

def delete_post(user_id: int, post_id: int):
    try:
        with Session(postgresql_engine) as session:
            statement = select(Post, User).join(User, User.id == Post.user_id).where(Post.id == post_id)
            post = session.execute(statement).scalars().first()

            if post is None:
                return HttpResponseModel(status_code=404, message="Post not found")

            if post.user_id != user_id:
                return HttpResponseModel(status_code=403, message="Unauthorized to delete post")

            session.delete(post)
            session.commit()

            return HttpResponseModel(status_code=200,
                                     message="Post deleted")
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))
    
def post_post(post_id: int, text: str):
    try:
        if len(text.strip()) == 0:
            return HttpResponseModel(status_code=400, message="Post text cannot be empty")
        
        if len(text) > 280:
            return HttpResponseModel(status_code=400, message="Post text cannot exceed 280 characters")

        with Session(postgresql_engine) as session:
            statement = select(User).where(User.id == post_id)
            user = session.execute(statement).scalars().first()

            if user is None:
                return HttpResponseModel(status_code=404, message="User not found")

            post = Post(user_id=post_id, text=text)
            session.add(post)
            session.commit()

            return HttpResponseModel(status_code=200, message="Post created")
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))

def load_feed(following: list[int]):
    try:
        if not following:
            return HttpResponseModel(status_code=200, message="User does not follow anyone", data=[])

        with Session(postgresql_engine) as session:
            statement = (
                select(Post)
                .join(User, User.id == Post.user_id)
                .where(Post.user_id.in_(following)) 
                .order_by(Post.date_time.desc())
            )
            posts = session.execute(statement).fetchall()

            if not posts:
                return HttpResponseModel(status_code=404, message="No posts were found")

            result = []
            for p in posts:
                p = p.Post
                post = PostPydantic(id=p.id,
                                    user_id=p.user_id,
                                    text=p.text,
                                    date_time=p.date_time).model_dump()
                result.append(post)

            return HttpResponseModel(
                status_code=200,
                message="Posts found",
                data=post_list
            )
    except Exception as e:
        return HttpResponseModel(
            status_code=500,
            message=str(e)
        )


def create_post(user_id: int, data: dict) -> HttpResponseModel:
    try:
        with Session(postgresql_engine) as session:
            post = Post(user_id=user_id,
                        text=data["text"],
                        location=data["location"],
                        hashtags=data["hashtags"])
            session.add(post)
            session.commit()
            session.refresh(post)

            post = PostPydantic(id=post.id,
                                user_id=post.user_id,
                                text=post.text,
                                location=post.location,
                                hashtags=post.hashtags,
                                date_time=post.date_time
                                ).model_dump()
            return HttpResponseModel(
                status_code=201,
                message="Post created",
                data=post
            )
    except Exception as e:
        return HttpResponseModel(
            status_code=500,
            message=str(e)
        )


def get_feed(user_id: int) -> HttpResponseModel:
    try:
        following = follow_service.get_following(user_id).data
        posts_list = []
        for user in following:
            posts_list += get_posts(user["id"]).data

        posts_list.sort(key=lambda x: x["date_time"], reverse=True)

        return HttpResponseModel(
            status_code=200,
            message="Feed retrieved successfully",
            data=posts_list
        )
    except Exception as e:
        return HttpResponseModel(status_code=500, message=str(e))
