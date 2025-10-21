# Libraries
from fastapi import APIRouter, Form, Depends
from starlette.requests import Request
from starlette.responses import JSONResponse
from passlib.hash import bcrypt
from tortoise.exceptions import IntegrityError
# Application Code
from backend.app.models import User
from backend.config import app
from backend.context import UserCtx
from backend.dependencies import get_current_user

router = APIRouter(
    prefix="", 
    tags=[""],
)
@router.get("/private/profile")
async def private_profile(request: Request, ctx: UserCtx = Depends(get_current_user)):
    return {"msg": "TODO"}

