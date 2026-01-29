from sqlmodel import SQLModel, Field, Column, func
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg

class UserBase(SQLModel):
    username:str = Field(index=True)
    email:str = Field(index=True, unique=True)

class User(UserBase, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    password: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=func.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=func.now(), onupdate=func.now()))

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserPublic(UserBase):
    id: int

class UserUpdate(UserBase):
    username: str | None = None
    password: str | None = Field(default=None, min_length=8)
