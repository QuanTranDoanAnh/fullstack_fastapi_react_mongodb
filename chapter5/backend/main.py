from decouple import config

DB_URL = config('DB_URL', cast=str)
DB_NAME = config('DB_NAME', cast=str)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from routers.cars import router as cars_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic before yield statement
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]
    yield
    # shutdown logic after yield statement
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(cars_router, prefix="/cars", tags=["cars"])

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True
    )