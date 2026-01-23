from fastapi import FastAPI

from app.routers import notifications, users

app = FastAPI(debug = True)
app.include_router(users.router)
app.include_router(notifications.router)

@app.get("/")
async def root():
    return{"mesaje":"Welcome to my first FastAPI API"}