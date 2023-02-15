from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from utils.jwt_manager import validate_token

user_email = "string"
user_pass = "string"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)

        if data['email'] != user_email:
            raise HTTPException(
                status_code=403, detail='Credentials are not valid')