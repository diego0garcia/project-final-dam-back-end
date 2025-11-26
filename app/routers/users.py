from fastapi import APIRouter, status, HTTPException, Header, Depends
from pydantic import BaseModel
from app.auth.auth import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.models import UserBase,UserDb,UserIn,UserLoginIn,UserOut
from app.database import UserDb
from app.auth.auth import create_access_token, verify_password

router = APIRouter(
    prefix="/users",
    tags=["Users"] #Esto es para la documentacion
)   

users: list[UserDb] = []

#Cuando accedas a /users/signup/ se ejecuta el seguiente metodo (created_user)
@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def created_user(userIn: UserIn):
    usersFound = [u for u in users if u.username == userIn.username]
    if len(usersFound) > 0:
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
    

@router.post("/login/", status_code=status.HTTP_200_OK)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    username: str | None = form_data.get("username")
    password: str | None = form_data.get("password")
    
    if username is None or password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username and/or password incorrect"
        )    
    
    usersFound = [u for u in users if u.username == username]
    
    if not usersFound:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Username and/or password incorrect"
        )
    
    user: UserDb = usersFound[0]
    if  verify_password(password, user.password):
            raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Username and/or password incorrect"
        )
    
    token = create_access_token(
        UserBase(
            username=user.username,
            password=user.password
        )
    )
    return token
    
#Cuando accedas a /users/signup/ se ejecuta el seguiente metodo (created_user)
@router.get("/{id}/", status_code=status.HTTP_201_CREATED)
async def get_user_by_id(id: int):
    pass


@router.get("/",response_model=list[UserOut],status_code=status.HTTP_200_OK)
async def get_all_users(authorization: str | None = Header()):
    print(authorization)
    
    parts = authorization.split(":")
    if len(parts) != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    
    if parts[0] != "mytoken":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
        
    payload_parts = parts[1].split("-")
    #Convierto un list[UserDb] en list[UserOut]
    return[
        
    ]
    
    username = payload_parts[0]
    if username not in [u.username for u in users]:
      raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="Forbidden"
      )  
    
    return [
        UserOut(id=UserDb.id, name=userDB.name, username=UserDb.username, email=UserDb.email, tlf=UserDb.tlf)
        for userDB in users]