from fastapi import FastAPI

from app.routers import users
from app.routers import studients

app = FastAPI(debug = True)
app.include_router(users.router)
app.include_router(studients.router)

@app.get("/")
async def root():
    return{"mesaje":"Welcome to my first FastAPI API"}