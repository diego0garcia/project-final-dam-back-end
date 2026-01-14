from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    password: str


class UserIn(UserBase):
    name: str
    email: str
    tlf: int
    
    
class UserDb(UserIn):
    id: int
    
    
class UserOut(BaseModel):
    id: int
    username: str
    name: str
    email: str
    tlf: int


#Es como un alias de UserBase pq esta vacio
class UserLoginIn(UserBase):
    pass
