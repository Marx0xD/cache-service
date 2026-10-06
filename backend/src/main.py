import uvicorn
from fastapi import FastAPI

from backend.src.db import Base, engine
from backend.src.routes.router import router

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
