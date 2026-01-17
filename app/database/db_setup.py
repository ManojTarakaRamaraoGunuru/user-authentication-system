from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from app.config import config


# Create async engine
# Create the database engine, echo puts the sql statements in the console log
engine = create_async_engine(
    config.DATABASE_URL,
    echo=True,  # Set to False in production
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

async def init_db():
    print("Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# We will create a FastAPI dependency with yield that will provide a new Session for each request. 
# This is what ensures that we use a single session per request.
def get_session():
    with Session(engine) as session:
        yield session


DbSession = Annotated[Session, Depends(get_session)]