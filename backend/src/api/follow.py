from fastapi import APIRouter, status
from src.schemas.response import HttpResponseModel
import src.service.impl.follow_service as follow_service

api = APIRouter()

@api.get("/{user_id}/following", response_model=HttpResponseModel)
def get_following(user_id: int):
    try:
        following = follow_service.get_following(user_id)
        return HttpResponseModel(status_code=status.HTTP_200_OK, message="OK", data=following)
    except Exception as e:
        return HttpResponseModel(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)) 


@api.get("/{user_id}/followers", response_model=HttpResponseModel)
def get_followers(user_id: int):
    try:
        followers = follow_service.get_followers(user_id)
        return HttpResponseModel(status_code=status.HTTP_200_OK, message="OK", data=followers)
    except Exception as e:
        return HttpResponseModel(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))


@api.post("/{follower_id}/follow/{followed_id}", response_model=HttpResponseModel)
def follow(follower_id: int, followed_id: int):
    try:
        result = follow_service.follow(follower_id, followed_id)
        return HttpResponseModel(status_code=status.HTTP_200_OK, message="OK", data=result)
    except Exception as e:
        return HttpResponseModel(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))


@api.post("/{follower_id}/unfollow/{followed_id}", response_model=HttpResponseModel)
def unfollow(follower_id: int, followed_id: int):
    try:
        result = follow_service.unfollow(follower_id, followed_id)
        return HttpResponseModel(status_code=status.HTTP_200_OK, message="OK", data=result)
    except Exception as e:
        return HttpResponseModel(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))
    

@api.post("/{requester_id}/accept_request/{requested_id}", response_model=HttpResponseModel)
def accept_follow_request(requester_id: int, requested_id: int):
    try:
        result = follow_service.accept_follow_request(requester_id, requested_id)
        return HttpResponseModel(status_code=status.HTTP_200_OK, message="OK", data=result)
    except Exception as e:
        return HttpResponseModel(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))
    

@api.post("/{requester_id}/reject_request/{requested_id}", response_model=HttpResponseModel)
def reject_follow_request(requester_id: int, requested_id: int):
    try:
        result = follow_service.reject_follow_request(requester_id, requested_id)
        return HttpResponseModel(status_code=status.HTTP_200_OK, message="OK", data=result)
    except Exception as e:
        return HttpResponseModel(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))
    

@api.get("/{user_id}/follow_requests_as_requester", response_model=HttpResponseModel)
def get_follow_requests_as_requester(user_id: int):
    try:
        result = follow_service.get_follow_requests_by_requester_id(user_id)
        return HttpResponseModel(status_code=status.HTTP_200_OK, message="OK", data=result)
    except Exception as e:
        return HttpResponseModel(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))


@api.get("/{user_id}/follow_requests_as_requested", response_model=HttpResponseModel)
def get_follow_requests_as_requested(user_id: int):
    try:
        result = follow_service.get_follow_requests_by_requested_id(user_id)
        return HttpResponseModel(status_code=status.HTTP_200_OK, message="OK", data=result)
    except Exception as e:
        return HttpResponseModel(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))