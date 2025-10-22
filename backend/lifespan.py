import os
import ssl
from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise import Tortoise
from backend.redis.redis import RedisAdapter

from dotenv import load_dotenv
import os

load_dotenv("backend/.env")

db_user = os.getenv("USER")
db_pass = os.getenv("PASSWORD")
db_name = os.getenv("DB")
db_host = os.getenv("HOST")
db_port = os.getenv("DB_PORT")

db_url = f"postgres://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    try: 
        await Tortoise.init(
            db_url=db_url,
            modules={"models": ["backend.app.models"]}
        )
        
        await Tortoise.generate_schema()
    except Exception as e:
        print(f"ERROR: failed to initialize database ({e})")

    redis_conn = RedisAdapter()
    app.state.kv_store = redis_conn 

    yield

    await redis_conn.flush()
    await redis_conn.close()
    await Tortoise.close_connections()
    
