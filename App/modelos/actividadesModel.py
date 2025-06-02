from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from modelos.usuariosModel import Salida

class ActividadInsert(BaseModel):
    nombre: str
    descripcion: str
    icono: str

class ActividadCompleta(ActividadInsert):
    idUsuario: str

class EliminarActividad(BaseModel):
    contrasena: str

class CambiarDatosActividad(BaseModel):
    contrasena : str
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    icono: Optional[str] = None

class ActividadSelect(BaseModel):
    idActividad:str
    idUsuario: str
    nombre: str
    descripcion: str
    icono: str

class ActividadesSalida(Salida):
    actividades: list[ActividadSelect]