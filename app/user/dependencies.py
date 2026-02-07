from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

class AccessTokenBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call_(self, request: Request) -> HTTPAuthorizationCredentials | None:
        
       creds = await super().__call__(request)