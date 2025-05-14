from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from modelos.usuariosModel import Salida

class EmocionSelect(BaseModel):
    nombre: str
    descripcion: str
    color:str
    idEmocion:str

class EmocionesSalida(Salida):
    emociones: list[EmocionSelect]