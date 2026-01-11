from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    username:str = Field(index=True)
    email:str = Field(index=True, unique=True)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserPublic(UserBase):
    id: int

class UserUpdate(UserBase):
    username: str | None = None
    password: str | None = Field(default=None, min_length=8)
