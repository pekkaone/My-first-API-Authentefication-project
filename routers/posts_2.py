from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from jose import JWTError
from db.models import Post
from db.database import get_session
from sqlmodel import Session, select

router = APIRouter()

class kurwaPost(BaseModel):
    id: int
    title: str
    content: str
    owner: str = None

class PostNew(BaseModel):
    id: int
    title: str
    content: str
    owner: str = None

class PostUpdate(BaseModel):
    id: Optional[int]
    title: Optional[str]
    content: Optional[str]
    owner: Optional[str] = None

@router.post("/create_post")
def create_post(post: Post, user: str = Depends(lambda: None), session: Session = Depends(get_session)):
    from auth_2 import current_user
    user = Depends(current_user)
    if user is None:
        raise HTTPException(status_code=401, detail='Ur token is bad')
    post.owner = user
    session.add(post)
    session.commit()
    session.refresh(post)

    return {"msg": "Post created"}

@router.get("/my_posts")
def show_user_posts(user: str = Depends(lambda: None), session: Session = Depends(get_session)):
    from auth_2 import current_user
    user = Depends(current_user)
    if user is not None:
        user_id = session.exec(select(Post).where())
        users_posts = session.get(select(Post))

        return users_posts
    raise HTTPException(status_code=400, detail="Bad user")

@router.delete("/delete_post/{post_id}")
def delete_user_post(post_id: int, user: str = Depends(lambda: None)):
    from auth_2 import current_user
    user = Depends(current_user)
    for post in Posts:
        if post.id == post_id:
            if post.owner != user:
                raise HTTPException(status_code=400, detail="You dont own dis post")
            Posts.remove(post)
            return {"post": "deleted"}
    raise HTTPException(status_code=400, detail="incorrect post id")
