from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select
from typing import Annotated

from app.database.db_setup import DbSession
from app.models.user import UserCreate, UserPublic, User, UserUpdate
from app.repositories.user import get_all_users, get_user_by_id, add_user, update_user, remove_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("", response_model=list[UserPublic])
def get_users(
    db_session: DbSession,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ):

    users = get_all_users(db_session, offset, limit)
    return users

@router.get("/{user_id}", response_model=UserPublic)
def get_user(
    user_id: int,
    db_session: DbSession
    ):

    user = get_user_by_id(db_session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id provided")
    return user

@router.post("", status_code=201, response_model=UserPublic)
def create_user(
    new_user: UserCreate, 
    db_session: DbSession
    ):
    
    new_user = User.model_validate(new_user)
    return add_user(db_session, new_user)

@router.patch("/{user_id}", status_code=200, response_model=UserPublic)
def patch_user(
    user_id: int,
    user_update: UserUpdate,
    db_session: DbSession
    ):

    user = get_user_by_id(db_session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the email provided")
    user = update_user(db_session, user, user_update)
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db_session: DbSession
    ):

    user = get_user_by_id(db_session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found with the id provided")
    remove_user(db_session, user)

    