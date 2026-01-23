from pydantic import BaseModel
    
class StudentDb():
    id: int


class StudentIn(StudentDb):
    dni: str
    name: str
    tlf: int
    email: str
    curso: str
    

class StudentOut(BaseModel):
    id: int
    nia: str
    name: str
    tlf: int
    email: str
    curso: str

