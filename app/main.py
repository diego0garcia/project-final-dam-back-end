from fastapi import FastAPI

from app.routers import notifications, users

app = FastAPI(debug = True)
app.include_router(users.router)
app.include_router(notifications.router)
from app.routers import users
from app.routers import students

app = FastAPI(debug = True)
app.include_router(users.router)
app.include_router(students.router)

@app.get("/")
async def root():
    return{"mesaje":"Welcome to my first FastAPI API"}