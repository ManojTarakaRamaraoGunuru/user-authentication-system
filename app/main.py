import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.user import routes as user_router
from app.tasks import routes as task_router
from app.database.db_setup import init_db

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

app.include_router(user_router.router)
app.include_router(task_router.router)

if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8000)