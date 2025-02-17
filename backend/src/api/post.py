from fastapi import APIRouter, status
from src.schemas.response import HttpResponseModel
import src.service.impl.post_service as post_service

api = APIRouter()


@api.post("/{user_id}/{text}", response_model=HttpResponseModel)
def publih_post(user_id: int, text: str):
    publish_post_response = post_service.post_post(user_id, text)
    return publish_post_response