from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from modelos.usuariosModel import Salida

class EntradaInsert(BaseModel):
    nota: str
    emocionesNumeros: list[int]
    actividad: str
    fecha: datetime | None = datetime.today()

class EntradaCompleta(EntradaInsert):
    idUsuario: str

class CambiarDatosEntrada(BaseModel):
    nota: str
    emocionesNumeros: list[str]
    actividad: str
    fecha : datetime | None = datetime.today()

class EntradaSelect(BaseModel):
    idEntrada:str
    idUsuario: str
    nota: str
    emociones: list[int]
    actividad: str
    Fecha: datetime

class EntradasSalida(Salida):
    entradas: list[EntradaSelect]
