from fastapi import APIRouter, status, HTTPException, Header, Depends
from pydantic import BaseModel
from app.auth.auth import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.database import UserDb, delete_notification_by_id, insert_notification, modify_notification, get_all_notification
from app.auth.auth import create_access_token, verify_password, oauth2_scheme, get_hash_password
from app.database import insert_user,get_notification_id, delete_user_by_id, get_all, get_user_by_username, modify_user, check_if_exists, get_id
from app.notification import NotificationDb, NotificationIn, NotificationOut
from app.routers import users

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)   

notifications: list[NotificationDb] = []

#Cuando accedas a /notifications/create/ se ejecuta el seguiente metodo (created_notification)
@router.post("/create/",status_code=status.HTTP_201_CREATED)
async def create_notification(notificationIn: NotificationIn):
    insert_notification(notificationIn)
    return notificationIn


#Get all
@router.get("/",response_model=list[NotificationOut],status_code=status.HTTP_200_OK)
async def get_all_notifications():
    notifications = []
    notifications = get_all_notification()
     
    if not notifications:
        raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="Forbidden"
        )  
    
    return notifications
    
#Modify notification
@router.put("/{id}/",status_code=status.HTTP_200_OK)
async def update_notification(id: int, nia_alumno: int = None, dni_usuario: int = None, descripcion: str = None, hora: str = None):
    
    notification = modify_notification(id, nia_alumno, dni_usuario, descripcion, hora)
    
    if notification is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Notification not found"
        )
    
    return notification

#Delete
@router.delete("/{id}/")
async def delete_notification(id: int, token: str = Depends(oauth2_scheme)):
    
    result = delete_notification_by_id(id)
    
    if result == 0:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Notification not already exists"
        )
    
    return result

@router.get("/{id}/", status_code=status.HTTP_201_CREATED)
async def get_notification_by_id(id: int):
    notification = get_notification_id(id)
    
    if notification is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Notification not already exists"
        )
    
    return notification