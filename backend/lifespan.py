import os
import ssl
from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise import Tortoise
from backend.redis.redis import RedisAdapter
from backend.app.models import User, Game

db_url = f"postgres://postgres:Unitheunicorn.00@127.0.0.1:5432/gameLib"

@asynccontextmanager
async def lifespan(app: FastAPI):
    try: 
        await Tortoise.init(
            db_url=db_url,
            modules={"models": ["backend.app.models.user", "backend.app.models.games"]}
        )
        
        await Tortoise.generate_schemas()
    except Exception as e:
        print(f"ERROR: failed to initialize database ({e})")

    redis_conn = RedisAdapter()
    app.state.kv_store = redis_conn 

    yield

    await redis_conn.flush()
    await redis_conn.close()
    await Tortoise.close_connections()
    
