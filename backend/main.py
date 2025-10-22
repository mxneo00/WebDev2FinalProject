# Python native
import os
# Dependency library
from fastapi import FastAPI, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from passlib.hash import bcrypt
# Application Code
from backend.config import app
from backend.session import Session, CSRFToken
from backend.lifespan import lifespan
from backend.app.models import User, Game
from backend.app.router import (auth, protected)
from backend.dependencies import get_current_user

app.include_router(auth.router)
app.include_router(protected.router)

templates = Jinja2Templates(directory="backend/public/html")

origins = [
    "http://localhost:8000",
]
app.add_middleware(
     CORSMiddleware,
     allow_origins=origins,  
    allow_credentials=True,
     allow_methods=["*"],  
     allow_headers=["*"],  
)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup")
async def read_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/login")
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "csrf_token": CSRFToken})

@app.get("/dashboard")
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/me")
async def read_me(request: Request):
    return {"msg" : "TODO"}

@app.get("/user")
async def get_users(request: Request):
    users = await User.all()

    users_response = []
    for user in users: 
        users_response.append({"username": user.username})
    return {"msg": "TODO"}

@app.get("/games")
async def get_games(request: Request):
    games = await Game.all()

    games_response = []
    for game in games:
        games_response.append({"gameTitle" : game.title})
    return {"msg": "TODO"}
