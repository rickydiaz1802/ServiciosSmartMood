from pydantic import BaseModel
from datetime import date, datetime

class UsuarioInsert(BaseModel):
    nombre: str
    contrasena: str
    correo: str
    edad: int
    FechaCreacion: datetime | None = datetime.today()

class Salida(BaseModel):
    mensaje: str

class UsuariosSalida(Salida):
    mensaje: str

