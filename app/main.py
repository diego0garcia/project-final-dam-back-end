from fastapi import FastAPI

from app.routers import users

app = FastAPI(debug = True)
app.include_router(users.router123)

@miapp.get("/")
async def root():
    return{"mesaje":"Welcome to my first FastAPI API"}