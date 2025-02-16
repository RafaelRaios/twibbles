from fastapi import APIRouter, status
from src.schemas.response import HttpResponseModel
import src.service.impl.user_service as user_service

api = APIRouter()


@api.get("/{user_id}", response_model=HttpResponseModel)
def get_user(user_id: int):
    try:
        user = user_service.get_user(user_id)
        if user is None:
            return HttpResponseModel(status_code=status.HTTP_404_NOT_FOUND, message="User not found")
        return HttpResponseModel(status_code=status.HTTP_200_OK, message="OK", data=user)
    except Exception as e:
        return HttpResponseModel(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e))

