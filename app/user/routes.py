from datetime import timedelta
from fastapi import APIRouter, Query, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import select
from typing import Annotated

from app.database.db_setup import DbSession
from app.user.models import UserCreate, UserPublic, User, UserUpdate, UserLogin
from app.user.service import UserService
from app.user.utils import create_access_token, verify_password

REFRESH_TOKEN_EXPIRY=2

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
user_repo = UserService()

@router.get("", response_model=list[UserPublic], status_code = status.HTTP_200_OK)
async def get_users(
    db_session: DbSession,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ):

    users =  await user_repo.get_all_users(db_session, offset, limit)
    return users

@router.get("/{user_id}", response_model=UserPublic, status_code = status.HTTP_200_OK)
async def get_user(
    user_id: int,
    db_session: DbSession
    ):

    user = await user_repo.get_user_by_id(db_session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id provided")
    return user

# Admin can create users
@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create_user(
    user: UserCreate, 
    db_session: DbSession
    ):
    
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )
    new_user = await user_repo.add_user(db_session, new_user)
    return new_user

@router.patch("/{user_id}", status_code = status.HTTP_200_OK, response_model=UserPublic)
async def patch_user(
    user_id: int,
    user_update: UserUpdate,
    db_session: DbSession
    ):

    user = await user_repo.get_user_by_id(db_session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the email provided")
    user = await user_repo.update_user(db_session, user, user_update)
    return user

@router.delete("/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db_session: DbSession
    ):

    user = await user_repo.get_user_by_id(db_session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id provided")
    await user_repo.remove_user(db_session, user)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def signup_user(
    user: UserCreate, 
    db_session: DbSession
    ):

    if await user_repo.is_user_exists(db_session, user.email):
        raise HTTPException(status_code=400, detail="User already exists with the email provided")
    
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )
    new_user = await user_repo.add_user(db_session, new_user)
    return new_user

@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    user_lgoin: UserLogin, 
    db_session: DbSession
):
    
    user_email = user_lgoin.email
    if not await user_repo.is_user_exists(db_session, user_email):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    user = await user_repo.get_user_by_email(db_session, user_email)
    if not verify_password(user_lgoin.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    data = {"user_id": str(user.id),
             "email": user.email}
    
    access_token = create_access_token(data)
    refresh_token = create_access_token(data, expiry=timedelta(days=REFRESH_TOKEN_EXPIRY), refresh=True)
    return JSONResponse(
            content = {
                "message": "Login Successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": user.id,
                    "email" : user.email,
                }
            }
    )

    