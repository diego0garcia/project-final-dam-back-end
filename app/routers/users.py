from fastapi import APIRouter, status, HTTPException, Header, Depends
from pydantic import BaseModel
from app.auth.auth import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.models import UserBase,UserDb,UserIn,UserLoginIn,UserOut
from app.database import UserDb
from app.auth.auth import create_access_token, verify_password, oauth2_scheme, TokenData
from app.database import insert_user, get_user_by_username
router = APIRouter(
    prefix="/users",
    tags=["Users"] #Esto es para la documentacion
)   

users: list[UserDb] = []

#Cuando accedas a /users/signup/ se ejecuta el seguiente metodo (created_user)
@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def created_user(userIn: UserIn):
    usersFound = [u for u in users if u.username == userIn.username]
    if usersFound:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Username already exists"
        )
    
    insert_user(
        UserDb(
            id = len(users) + 1,
            username = userIn.username,
            name=userIn.name,
            email = userIn.email,
            tlf = userIn.tlf,
            password = userIn.password
        )
    )
    

@router.post("/login/", status_code=status.HTTP_200_OK)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    username: str | None = form_data.username
    password: str | None = form_data.password
    
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
    if not verify_password(password, user.password):
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
async def get_all_users(token: str = Depends(oauth2_scheme)):#authorization: str | None = Header()):
    data: TokenData = decode_token(token)
     
    if data.username not in [u.username for u in users]:
      raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="Forbidden"
      )  
    
    return [
        UserOut(id=UserDb.id, name=userDB.name, username=UserDb.username, email=UserDb.email, tlf=UserDb.tlf)
        for userDB in users
    ]