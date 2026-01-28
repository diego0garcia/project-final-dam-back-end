from fastapi import APIRouter, status, HTTPException, Depends
from app.studient import StudentIn, StudentOut
from app.auth.auth import oauth2_scheme
from app.database import insert_studient, check_studient_if_exists, get_by_id_studient, get_student_by_username, get_all_studient, modify_studient, delete_studient_by_id

router = APIRouter(
    prefix="/students",
    tags=["Students"] #Esto es para la documentacion
)   


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(studientIn: StudentIn):
    if check_studient_if_exists(studientIn.nia):
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "NIA already exists"
        )
    
    insert_studient(studientIn)


@router.get("/{id}/", status_code=status.HTTP_201_CREATED)
async def get_studient_by_id(id: int):
    studient = get_by_id_studient(id)
    
    if studient is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "User not already exists"
        )
    
    return studient


@router.get("/username/{username}/", status_code=status.HTTP_201_CREATED)
async def get_user_by_name(username: str):
    student = get_student_by_username(username)
    
    if student is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Student not already exists"
        )
    
    return student


@router.get("/",response_model=list[StudentOut],status_code=status.HTTP_200_OK)
async def get_all_studients():
    studients = []
    studients = get_all_studient()
     
    if not studients:
        raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="Forbidden"
        )  
    
    return studients


#Modify
@router.put("/{id}/", status_code=status.HTTP_200_OK)
async def update_studient(id: int, nia:str = None, name:str = None, tlf:int = None, email:str = None, course:str = None):    
    studient = modify_studient(id, nia, name, tlf, email, course)
    
    if studient is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Student not found"
        )
    
    return studient


#Delete
@router.delete("/{id}/")
async def delete_studient(id: int, token: str = Depends(oauth2_scheme)):
    result = delete_studient_by_id(id)
    
    if result == 0:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Student not already exists"
        )
    
    return result