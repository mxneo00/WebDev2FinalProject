import os
from typing import Any
# Libraries
from fastapi import FastAPI
# Application Code
from backend.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

DATABASE_URL: str = "postgres://postgres:postgres@localhost:5432/postgres"
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SESSION_COOKIE: str = "sid"
SESSION_TTL_SECONDS: int = 60*60*24*7
CORS_ORIGINS: list[Any] = ["http://localhost:3000"]
SECRET_KEY: str = "dev-secret"  # use env var in prod