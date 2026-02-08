from datetime import datetime, timezone
from pydantic import BaseModel, field_validator
from sqlalchemy import DateTime
from sqlmodel import SQLModel, Field, func, Column
from sqlalchemy.sql.schema import ForeignKey



class Task(SQLModel, table=True):

    __tablename__ = 'tasks'

    id:int = Field(primary_key=True, default = None)
    user_id: int = Field(sa_column=Column(ForeignKey("users.id", ondelete="CASCADE")))
    title: str
    descritpion: str
    status: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
        )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
        )

class CreateOrUpdateTask(BaseModel):
    title: str
    descritpion: str
    status: str
    
    @field_validator('title')
    def check_title(cls, value):
        if len(value) > 15:
            raise ValueError("Maximum allowed title length is 15")