from src.engine import postgresql_engine
from sqlalchemy.orm import Session
from model.sqlalchemy.user import User
from model.sqlalchemy.following import Following
from model.sqlalchemy.follow_requests import FollowRequest
from model.pydantic.user import User as UserPydantic

from src.service.impl.user_service import get_user

from sqlalchemy import select


def get_following(user_id: int):
    with Session(postgresql_engine) as session:
        statement = select(Following, User).join(User, Following.followed_id == User.id).where(Following.follower_id == user_id)
        following = session.execute(statement).fetchall()
        result = []
        for f in following:
            f = f.User
            result.append(UserPydantic(id=f.id,
                                       user_name=f.user_name,
                                       email=f.email,
                                       is_private=f.is_private))

        return {"status": "ok", "data": result}


def get_followers(user_id: int):
    with Session(postgresql_engine) as session:
        statement = select(Following, User).join(User, Following.follower_id == User.id).where(Following.followed_id == user_id)
        followers = session.execute(statement).fetchall()
        result = []
        for f in followers:
            f = f.User
            result.append(UserPydantic(id=f.id,
                                       user_name=f.user_name,
                                       email=f.email,
                                       is_private=f.is_private))

        return {"status": "ok", "data": result}


def follow(follower_id: int, followed_id: int):
    with Session(postgresql_engine) as session:
        # check if the user is already following
        statement = select(Following).where(Following.follower_id == follower_id, Following.followed_id == followed_id)
        following = session.execute(statement).fetchone()
        if following is not None:
            return {"status": "error", "message": "User is already following"}

        # first check if the user is private or not
        followed_user = get_user(followed_id)["data"]

        if followed_user.is_private:
            request_follow(follower_id, followed_id)
            return {"status": "success", "message": "Follow request sent"}
        session.add(Following(follower_id=follower_id, followed_id=followed_id))
        session.commit()
        return {"status": "success", "message": "Followed successfully"}


def request_follow(follower_id: int, followed_id: int):
    with Session(postgresql_engine) as session:
        session.add(FollowRequest(requester_id=int(follower_id), requested_id=int(followed_id)))
        session.commit()
        return {"status": "success", "message": "Follow request sent"}


def accept_follow_request(requester_id: int, requested_id: int):
    with Session(postgresql_engine) as session:
        statement = select(FollowRequest).where(FollowRequest.requester_id == requester_id, FollowRequest.requested_id == requested_id)
        follow_request = session.execute(statement).fetchone()
        if follow_request is None:
            return {"status": "error", "message": "Follow request not found"}
        follow_request = follow_request[0]
        session.delete(follow_request)
        session.add(Following(follower_id=int(requester_id), followed_id=int(requested_id)))
        session.commit()
        return {"status": "success", "message": "Followed successfully"}


def reject_follow_request(requester_id: int, requested_id: int):
    with Session(postgresql_engine) as session:
        statement = select(FollowRequest).where(FollowRequest.requester_id == requester_id, FollowRequest.requested_id == requested_id)
        follow_request = session.execute(statement).fetchone()
        if follow_request is None:
            return {"status": "error", "message": "Follow request not found"}
        follow_request = follow_request[0]
        session.delete(follow_request)
        session.commit()
        return {"status": "success", "message": "Follow request rejected"}


def unfollow(follower_id: int, followed_id: int):
    with Session(postgresql_engine) as session:
        statement = select(Following).where(Following.follower_id == follower_id, Following.followed_id == followed_id)
        following = session.execute(statement).fetchone()
        if following is None:
            return {"status": "error", "message": "User is not following"}
        following = following[0]
        session.delete(following)
        session.commit()
        return {"status": "success", "message": "Unfollowed successfully"}


def get_follow_requests_by_requester_id(requester_id: int):
    with Session(postgresql_engine) as session:
        statement = select(FollowRequest).where(FollowRequest.requester_id == requester_id)
        follow_requests = session.execute(statement).fetchall()
        result = []
        for f in follow_requests:
            f = f.FollowRequest
            result.append({"requester_id": f.requester_id,
                           "requested_id": f.requested_id})
        return {"status": "ok", "data": result}


def get_follow_requests_by_requested_id(requested_id: int):
    with Session(postgresql_engine) as session:
        statement = select(FollowRequest).where(FollowRequest.requested_id == requested_id)
        follow_requests = session.execute(statement).fetchall()
        result = []
        for f in follow_requests:
            f = f.FollowRequest
            result.append({"requester_id": f.requester_id,
                           "requested_id": f.requested_id})
        return {"status": "ok", "data": result}
