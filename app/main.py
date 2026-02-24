import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.user import routes as user_router
from app.tasks import routes as task_router
from app.exceptions.exception_handler import register_exceptions
from app.database.db_setup import init_db
from app.database.redis import redis_client
from app.middleware import register_middlewares

@asynccontextmanager
async def life_span(app: FastAPI):
    print("server is starting up...")
    await init_db()
    await redis_client.initialize()
    yield
    print("server is shutting down...")
    await redis_client.close()

app = FastAPI(
    lifespan = life_span,
    description= "Task management system",
    version = "v1",
    docs_url = "/docs",
    contact = {
        "email" : "Apple.123@gmail.com"
    }
)

register_exceptions(app)
register_middlewares(app)

@app.get("/health", tags=["health"])
def health():
    return {"data": "Health looks good"}

app.include_router(user_router.router)
app.include_router(task_router.router)

if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8000)