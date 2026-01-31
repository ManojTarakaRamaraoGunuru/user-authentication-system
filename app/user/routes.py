from fastapi import APIRouter, Query, HTTPException, status
from sqlmodel import select
from typing import Annotated

from app.database.db_setup import DbSession
from app.user.models import UserCreate, UserPublic, User, UserUpdate
from app.user.service import UserService

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

    if user_repo.is_user_exists(db_session, user.email):
        raise HTTPException(status_code=400, detail="User already exists with the email provided")
    
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )
    new_user = await user_repo.add_user(db_session, new_user)
    return new_user    