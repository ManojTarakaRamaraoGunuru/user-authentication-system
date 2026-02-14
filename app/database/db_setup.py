from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from app.config import config


# Create async engine
# Create the database engine, echo puts the sql statements in the console log
engine = create_async_engine(
    config.DATABASE_URL,
    echo=False,  # Set to False in production
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
async def get_session():
    async_session = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

    async with async_session() as session:
        yield session


DbSession = Annotated[AsyncSession, Depends(get_session)]