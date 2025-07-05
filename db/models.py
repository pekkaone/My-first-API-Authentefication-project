from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    owner_id: int = Field(foreign_key="user.id")
    owner: Optional['User'] = Relationship(back_populates='posts')

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username:str
    password:str
    posts: List[Post] = Relationship(back_populates="owner")


