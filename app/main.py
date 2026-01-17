import uvicorn

from fastapi import FastAPI

from app.routes import user
from app.database.db_setup import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app: FastAPI):
    print("server is starting up...")
    await init_db()
    yield
    print("server is shutting down...")

app = FastAPI(
    lifespan = life_span
)

@app.get("/health", tags=["health"])
def health():
    return {"data": "Health looks good"}

app.include_router(user.router)

if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8000)