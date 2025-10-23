import os
import ssl
from contextlib import asynccontextmanager
from fastapi import FastAPI
from tortoise import Tortoise
from backend.redis.redis import RedisAdapter
#from backend.app.models import User, Game

db_url = f"postgres://postgres:Unitheunicorn.00@localhost:5432/gameLib"

@asynccontextmanager
async def lifespan(app: FastAPI):
    try: 
        import backend.app.models
        print("Loaded models:", backend.app.models.__all__)
        print("Initializing Tortoise ORM...")
        await Tortoise.init(
            db_url="postgres://postgres:Unitheunicorn.00@localhost:5432/gameLib",
            modules={"models": ["backend.app.models"]}
        )
        await Tortoise.generate_schemas()
        print("✅ Database initialized successfully.")
    except Exception as e:
        print(f"ERROR: failed to initialize database ({e})")

    redis_conn = RedisAdapter()
    app.state.kv_store = redis_conn 

    yield

    await redis_conn.flush()
    await redis_conn.close()
    await Tortoise.close_connections()
    
