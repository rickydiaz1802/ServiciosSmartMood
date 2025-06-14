from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class UsuarioInsert(BaseModel):
    nombre: str
    contrasena: str
    correo: str
    edad: int
    FechaCreacion: datetime | None = datetime.today()
    tipo: str

class Salida(BaseModel):
    mensaje: str

class EliminarUsuario(BaseModel):
    contrasena: str

class CambiarContrasena(BaseModel):
    contrasenaAnterior: str
    contrasenaNueva: str

class CambiarDatos(BaseModel):
    contrasena: str
    nombre: Optional[str] = None
    correo: Optional[str] = None
    edad: Optional[int] = None

class UsuarioSelect(BaseModel):
    idUsuario:str
    nombre: str
    contrasena: str
    correo: str
    edad: int
    FechaCreacion: datetime
    tipo: str

class UsuariosSalida(Salida):
    usuarios: list[UsuarioSelect]

