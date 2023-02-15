from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from schemas.user import User

user_email = "string"
user_pass = "string"

user_router = APIRouter()


@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == user_email and user.password == user_pass:
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
