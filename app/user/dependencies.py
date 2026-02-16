from fastapi import Request, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import HTTPException, status
from typing import List

from app.user.utils import decode_access_token
from app.user.service import UserService
from app.database.redis import is_jti_blocklisted
from app.database.db_setup import DbSession

user_service = UserService()

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

class RoleChecker:

    def __init__(self, allowed_roles:List[str]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, 
                 token = Depends(AccessTokenBearer()),
                 session = DbSession,
                 ):
        
        user = user_service.get_user_by_email(session, token['email'])
        if user.role in self.allowed_roles:
            return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not allowed to access it")

# Admin role
admin_role = RoleChecker(["admin"])
user_role = RoleChecker(["user"])