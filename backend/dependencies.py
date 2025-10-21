# Libararies
from fastapi import Depends, HTTPException
from starlette.requests import Request
from tortoise.exceptions import DoesNotExist
# Application Code
from backend.redis.redis import RedisAdapter
from backend.session import Session, SessionManager
from backend.context import UserCtx, AdminCtx
from backend.app.models import User

def get_kv_store(request: Request) -> RedisAdapter:
    return request.app.state.kv_store

def get_session_manager(request: Request) -> SessionManager:
    return request.app.state.session_manager

def get_session(
    request: Request, session_manager: SessionManager = Depends(get_session_manager)
) -> Session:
    if not hasattr(request.state, "session"):
        request.state.session = Session(
            request=request, session_manager=session_manager #Change
        )
    return request.state.session

async def get_current_user(request: Request, session: Session = Depends(get_session)):
    await session.load()
    if not session.data or not session.data.get("user_id"):
        raise HTTPException(status_code=303, headers={"location": "/"})

    try:
        user = await User.get(user_id=session.data["user_id"])
        user = UserCtx(user, session)

    except DoesNotExist as e:
        raise HTTPException(status_code=303, headers={"location": "/"}) from e
    return user

def get_admin(request: Request, ctx: UserCtx = Depends(get_current_user)):
    try:
        admin = AdminCtx(ctx.user, ctx.session)
    except PermissionError as e:
        raise HTTPException(status_code=401, detail="Not authenticated") from e
    return admin