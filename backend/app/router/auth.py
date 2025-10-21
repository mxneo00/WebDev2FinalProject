# Libraries
from passlib.hash import bcrypt
from fastapi import FastAPI, Form, Depends
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import JSONResponse
from tortoise.exceptions import IntegrityError
# Application Code
from backend.session import Session
from backend.lifespan import lifespan
from backend.app.models import User
from backend.config import app

router = APIRouter(prefix="/auth",tags=['auth'],)

templates = Jinja2Templates(directory="backend/public/html")

@router.get("/signup")
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
async def post_signup(
    fname = Form(...),
    lname = Form(...),
    email = Form(...),
    username = Form(...),
    password = Form(...),
    password_confirmation = Form(...),
):
    if password != password_confirmation:
        return JSONResponse({"error": "Passwords do not match"})
    try:
        user = await User.create(
            username=username,
            fname=fname, 
            lname=lname, 
            email=email,
            digest=bcrypt.hash(password),
            role="temp",
            tier="free",
        )
    except IntegrityError as e:
        print("FAILED TO CREATE USER")
    return {"msg": "TODO"}

@router.get("/me")
async def get_me(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JSONResponse({"error": "Not authenticated"})
    user = await User.get_or_none(id=user_id)
    return {"user": user.username, "email": user.email}

@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    user = await User.get_or_none(email=email)
    if not user or not bcrypt.verify(password, user.digest):
        return JSONResponse({"error": "Invalid login"})
    request.session["user_id"] = user.id
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return templates.TemplateResponse("login.html", {"request": request})