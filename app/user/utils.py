import jwt
import datetime
import uuid
from app.config import Config
from passlib.context import CryptContext
from datetime import timedelta

ACCESS_TOKEN_EXPIRY=3600 # seconds
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expiry: timedelta, refresh: bool = False) -> str:
    payload = {}

    payload["user"] = data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["jti"] = str(uuid.uuid4()) # unique identifier for the json token
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )
    return token

def decode_access_token(token: str) -> dict | None:

    try:
        payload = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )
        return payload
    except jwt.PyJWTError as e:
        print(e)
        return None