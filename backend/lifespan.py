import os
import ssl
from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise import Tortoise
from backend.redis.redis import RedisAdapter

@asynccontextmanager
async def lifespan(app: FastAPI):
    try: 
        await Tortoise.init(
            db_url=f"postgres://{os.getenv("user")}:{os.getenv("password")}@localhost:5432/{os.getenv("DB")}",
            modules={"models": ["app.models"]}
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
    
