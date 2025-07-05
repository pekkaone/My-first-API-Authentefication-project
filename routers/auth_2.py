from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from typing import Optional, List
from datetime import datetime, timedelta
from sqlmodel import select, Session
from db.models import User
from db.database import get_session

route = APIRouter()

ALGORITHM = "HS256"
SECRET_KEY = "BEBEBEBE"
ACCES_TIME_EXPIRING = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_type: str
    token_type: str = "Bearer"

def create_access_token(data: dict):
    needencode = data.copy()
    expires = datetime.now() + timedelta(minute=ACCES_TIME_EXPIRING)
    needencode.update({"exp": expires})
    jwt_encoded = jwt.encode(needencode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_encoded

@route.post("/authentefication")
def auth(user: User, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == user.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Nickname is alreafy taken")
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"msg": "user authended", "name": user.username, "password": "*******"}

@route.post("/login")
def login(user: User, session: Session = Depends(get_session)):
    right_login = session.exec(select(User).where((User.username == user.username) & (User.password == user.password))).first
    if right_login:
        token = create_access_token(data={"sub": user.username, "ids": user.id})
        return {"Access type": token, "token_type": "Bearer"}
    raise HTTPException(status_code=401, detail="Incorrect name or password")

def current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user = payload.get("sub")
        if user is None:
            raise HTTPException(status_code=401, detail="No name bitch")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Big error")
    
@route.get("/me")
def current_logined_user(user: str = Depends(current_user), user_posts: list = Depends(lambda: None)):
    from posts_2 import show_user_posts
    user_posts = Depends(show_user_posts)
    return {"name": user, "Posts": user_posts}
