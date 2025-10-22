# Libraries
from fastapi import APIRouter, Form, Depends
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import JSONResponse
from passlib.hash import bcrypt
from tortoise.exceptions import IntegrityError
# Application Code
from backend.app.models import User, Game
from backend.config import app
from backend.context import UserCtx
from backend.dependencies import get_current_user

router = APIRouter(prefix="", tags=[""])
templates = Jinja2Templates(directory = "backend/public/html")
#------------------------DASHBOARD----------------------------
@router.get("/dashboard")
async def dashboard(request: Request, ctx: UserCtx = Depends(get_current_user)):
    # Query all games by owner
    games = await Game.filter(owner_id = ctx.user.user_id).all()
    return templates.TemplateResponse("dashboard.html", {"request":request, "user":ctx.user, "games":games,})
#------------------------PROFILE------------------------------
@router.get("/private/profile")
async def private_profile(request: Request, ctx: UserCtx = Depends(get_current_user)):
    return {"msg": "TODO"}

