# Libraries
from passlib.hash import bcrypt
from fastapi import FastAPI, Form, Depends
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from tortoise.exceptions import IntegrityError
# Application Code
from backend.session import Session
from backend.lifespan import lifespan
from backend.app.models import User
from backend.config import app

router = APIRouter(prefix="",tags=['auth'],)
templates = Jinja2Templates(directory="backend/public/html")
#---------------------SIGNUP--------------------------------
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
        return JSONResponse({"error": "Passwords must match"}, status_code = 400)
    try:
        user = await User.create(
            username=username,
            fname=fname, 
            lname=lname, 
            email=email,
            digest=bcrypt.hash(password)
        )
    except IntegrityError as e:
        JSONResponse({"error": "Failed to create user"}, status_code = 400)
    return RedirectResponse(url = "/dashboard")
#-----------------LOGIN---------------------------------
@router.post("/login")
async def post_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    user = await User.get_or_none(email=email)
    if not user or not bcrypt.verify(password, user.digest):
        return JSONResponse({"error": "Invalid login"}, status_code = 401)
    request.session["user_id"] = user.id
    return RedirectResponse(url = "/dashboard", status_code = 302)

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url = "/login", status_code = 302)
#-----------------USERDATA------------------------
@router.get("/me")
async def get_me(request: Request):
    session = Session(request)
    data = await session.get_session()
    if not data:
        return JSONResponse({"error": "Not authenticated"}, status_code = 401)
    return JSONResponse({"user": data})