from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session
from app.config import config

db_url = config.DATABASE_URL

connect_args = {"check_same_thread": False}
engine = create_engine(db_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# We will create a FastAPI dependency with yield that will provide a new Session for each request. 
# This is what ensures that we use a single session per request.
def get_session():
    with Session(engine) as session:
        yield session


DbSession = Annotated[Session, Depends(get_session)]