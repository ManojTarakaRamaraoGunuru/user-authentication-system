from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import HTTPException, status

from app.user.utils import decode_access_token
from app.database.redis import is_jti_blocklisted

class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> dict:

       creds = await super().__call__(request)

       ## creds contains scheme=HTTPBearer, credentials
       token = decode_access_token(creds.credentials)
    
       if await is_jti_blocklisted(token["jti"]):
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired, please re login")

       self.verify_token(token)
       
       return token
    
    def verify_token(self, token:dict):
        raise NotImplementedError("Implement this method")

class AccessTokenBearer(TokenBearer):

    def verify_token(self, token:dict):

        if token and token["refresh"]:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Please provide an acess token")

class RefreshTokenBearer(TokenBearer):

    def verify_token(self, token:dict):

        if token and not token["refresh"]:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail="Please provide an refresh token")
