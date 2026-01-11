import uvicorn

from fastapi import FastAPI

from app.routes import user
from app.database.db_setup import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/health", tags=["health"])
def health():
    return {"data": "Health looks good"}

app.include_router(user.router)

if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8000)