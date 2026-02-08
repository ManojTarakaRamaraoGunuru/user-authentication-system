from datetime import datetime, timezone
from enum import Enum
import string
from pydantic import BaseModel, field_validator
from sqlalchemy import DateTime
from sqlmodel import SQLModel, Field, func, Column
from sqlalchemy.sql.schema import ForeignKey



class Task(SQLModel, table=True):

    __tablename__ = 'tasks'

    id:int = Field(primary_key=True, default = None)
    user_id: int = Field(sa_column=Column(ForeignKey("users.id", ondelete="CASCADE")))
    title: str
    description: str
    status: int
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
        )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
        )

class TaskStatus(int, Enum):
    CREATED = 1
    IN_PROGRESS = 2
    COMPLETED = 3  

class CreateTask(BaseModel):
    title: str = Field(max_length=15)
    description: str
    status: TaskStatus
    
    @field_validator('title')
    def validate_title(cls, value):

        allowed_chars = string.ascii_letters + string.digits + ' '
        # Check each character
        for char in value:
            if char not in allowed_chars:
                raise ValueError(
                    f"Title contains invalid character: '{char}'. "
                    f"Only letters, numbers, and spaces are allowed."
                )
        
        return value ## required otherwise title will be set to None

class UpdateTask(BaseModel):
    title: str | None = Field(default=None, max_length=15)
    description: str | None = None
    status: TaskStatus | None =  None
    
    @field_validator('title')
    def validate_title(cls, value):

        if value is None:
            return None

        allowed_chars = string.ascii_letters + string.digits + ' '
        # Check each character
        for char in value:
            if char not in allowed_chars:
                raise ValueError(
                    f"Title contains invalid character: '{char}'. "
                    f"Only letters, numbers, and spaces are allowed."
                )
        
        return value ## required otherwise title will be set to None

class TaskPublic(BaseModel):
    id : int
    title: str
    description: str
    created_at : datetime
    updated_at : datetime
    status: TaskStatus
