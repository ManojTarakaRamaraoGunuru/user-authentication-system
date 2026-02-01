from sqlmodel import SQLModel, Field, Column, func
from datetime import datetime
from sqlalchemy import DateTime
from datetime import timezone

class UserBase(SQLModel):
    username:str = Field(index=True)
    email:str = Field(index=True, unique=True)

class User(UserBase, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    password: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
        )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
        )

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserPublic(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

class UserUpdate(UserBase):
    username: str | None = None
    password: str | None = Field(default=None, min_length=8)

class UserLogin(SQLModel):
    email: str
    password: str
