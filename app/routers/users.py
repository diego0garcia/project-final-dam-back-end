from fastapi import APIRouter, status, HTTPException, Header, Depends
from pydantic import BaseModel
from app.auth.auth import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.models import UserBase,UserDb,UserIn,UserLoginIn,UserOut
from app.database import UserDb
from app.auth.auth import create_access_token, verify_password, oauth2_scheme, get_hash_password
from app.database import insert_user, get_by_id, delete_user_by_id, get_all, get_user_by_username, modify_user, check_if_exists, get_id

router = APIRouter(
    prefix="/users",
    tags=["Users"] #Esto es para la documentacion
)   

users: list[UserDb] = []

#Cuando accedas a /users/signup/ se ejecuta el seguiente metodo (created_user)
@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def sign_up_user(userIn: UserIn):
    
    if check_if_exists(userIn.username):
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Username already exists"
        )
    
    userIn.password = get_hash_password(userIn.password)
    insert_user(userIn)


@router.post("/login/", status_code=status.HTTP_200_OK)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
#async def login_user(user: UserIn):
    username: str | None = form_data.username
    password: str | None = form_data.password
    
    if username is None or password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username and/or password incorrect"
        )    
    
    userDb = get_user_by_username(username)
    if not userDb:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Username don't exists"
        )
    
    if not verify_password(password, userDb.password):
            raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Username and/or password incorrect"
            )
    
    token = create_access_token(
        UserBase(
            username=form_data.username,
            password=form_data.password
        )
    )
    return token
    
    
#Cuando accedas a /users/signup/ se ejecuta el seguiente metodo (created_user)
@router.get("/{id}/", status_code=status.HTTP_201_CREATED)
async def get_user_by_id(id: int):
    user = get_by_id(id)
    
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "User not already exists"
        )
    
    return user

@router.get("/username/{username}/", status_code=status.HTTP_201_CREATED)
async def get_user_by_name(username: str):
    user = get_user_by_username(username)
    
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "User not already exists"
        )
    
    return user


@router.get("/",response_model=list[UserOut],status_code=status.HTTP_200_OK)
#async def get_all_users(token: str = Depends(oauth2_scheme)):#authorization: str | None = Header()):
async def get_all_users():
    users = []
    users = get_all()
     
    if not users:
        raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="Forbidden"
        )  
    
    return users
    
#Modify
@router.put("/{id}/", status_code=status.HTTP_200_OK)
async def update_user(id: int, dni:str = None, name:str = None, username:str = None, email:str = None, tlf:int = None, password:str = None):
    
    if password:
        password = get_hash_password(password)
    user = modify_user(id, dni, name, username, email, tlf, password)
    
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )
    
    return user

#Delete
@router.delete("/{id}")
async def delete_user(id: int, token: str = Depends(oauth2_scheme)):
    
    result = delete_user_by_id(id)
    
    if result == 0:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "User not already exists"
        )
    
    return result

#User if is superadmin can create other user