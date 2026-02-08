from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import HTTPException, status

from app.user.utils import decode_access_token

class AccessTokenBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        
       creds = await super().__call__(request)

       ## creds contains scheme=HTTPBearer, credentials
       token = decode_access_token(creds.credentials)

       if token == None or token["refresh"]:
           raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, details="Token expired")
       
       return token
           