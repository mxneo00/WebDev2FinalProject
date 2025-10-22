import os
from typing import Any
# Libraries
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
# Application Code
from backend.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

# register_tortoise(
#         app,
#         db_url="postgres://postgres:Unitheunicorn.00@127.0.0.1:5432/gameLib",
#         modules={"models": ["backend.app.models.user", "backend.app.models.games"]},
#         generate_schemas = True,
#         add_exception_handlers = True,
#     )

DATABASE_URL: str = "postgres://postgres:Unitheunicorn.00@127.0.0.1:5432/gameLib"
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SESSION_COOKIE: str = "sid"
SESSION_TTL_SECONDS: int = 60*60*24*7
CORS_ORIGINS: list[Any] = ["http://localhost:3000"]
SECRET_KEY: str = "dev-secret"  # use env var in prod