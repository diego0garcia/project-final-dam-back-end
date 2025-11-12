from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

router123 = APIRouter(
    prefix="/users",
    tags=["Users"] #Esto es para la documentacion
)

class UserDb(BaseModel):
    id: int
    name: str
    email: str
    tlf: int
    password: str

class UserIn(BaseModel):
    name: str
    email: str
    tlf: int
    password: str

users: list[UserDb] = []

#Cuando accedas a /users/signup/ se ejecuta el seguiente metodo (created_user)
@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def created_user(userIn: UserIn):
    usersFound = [u for u in users if u.name == userIn.name]
    if len(userFound) > 0:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Username already exists"
        )
    
    users.append(
        UserDb(
            id = len(users) + 1,
            name=userIn.name,
            email = userIn.email,
            tlf = userIn.tlf,
            password = UserIn.password
        )
    )

#Cuando accedas a /users/signup/ se ejecuta el seguiente metodo (created_user)
@router.get("/{id}/", status_code=status.HTTP_201_CREATED)
async def get_user_by_id(id: int):
    pass