from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

router123 = APIRouter(
    prefix="/users",
    tags=["Users"] #Esto es para la documentacion
)


class UserBase(BaseModel):
    username: str
    password: str

class UserIn(UserBase):
    name: str
    email: str
    tlf: int
    password: str
    
class UserDb(UserIn):
    id: int

#Es como un alias de UserBase pq esta vacio
class UserLoginIn(UserBase):
    pass
    
class TokenOut(BaseModel):
    token: str

users: list[UserDb] = []

#Cuando accedas a /users/signup/ se ejecuta el seguiente metodo (created_user)
@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def created_user(userIn: UserIn):
    usersFound = [u for u in users if u.username == userIn.username]
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

@router.post("/login/",response_model=TokenOut, status_code=status.HTTP_200_OK)
async def login_user(userLoginIn: UserLoginIn):
    usersFound = [u for u in users if u.username == userLoginIn.username]
    if not usersFound:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Username and/or password incorrect"
        )
        
    user: UserDb = usersFound[0]
    if user.password != userLoginIn.password:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Username and/or password incorrect"
        )
    
    return TokenOut(token=f"mytoken:{user.username}-{user.password}")
    
#Cuando accedas a /users/signup/ se ejecuta el seguiente metodo (created_user)
@router.get("/{id}/", status_code=status.HTTP_201_CREATED)
async def get_user_by_id(id: int):
    pass