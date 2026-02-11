from pydantic import BaseModel
    
class StudentIn(BaseModel):
    nia: int
    name: str
    tlf: int
    email: str
    course: str

    
class StudentDb(StudentIn):
    id: int


class StudentOut(BaseModel):
    id: int
    nia: str
    name: str
    tlf: int
    email: str
    course: str
    
    