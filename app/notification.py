from datetime import datetime
from pydantic import BaseModel

class NotificationDb(BaseModel):
    id: int


class NotificationIn(NotificationDb):
    nia_alumno: int
    dni_usuario: str
    descripcion: str
    hora: datetime


class NotificationOut(BaseModel):
    id: int
    nia_alumno: int
    dni_usuario: str
    descripcion: str
    hora: datetime

