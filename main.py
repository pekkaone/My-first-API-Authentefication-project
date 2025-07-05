from fastapi import FastAPI
from routers import posts_2, auth_2
from db.database import create_db_and_tables

app = FastAPI()

create_db_and_tables()
app.include_router(posts_2.router, prefix="/posts", tags=["Posts"])
app.include_router(auth_2.route, prefix="/auth", tags=["Auth"])

