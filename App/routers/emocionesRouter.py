from fastapi import APIRouter, Request, Depends
from dao.emocionesDAO import EmocionesDAO
from modelos.emocionesModel import EmocionesSalida
from modelos.usuariosModel import UsuarioSelect
from routers.usuariosRouter import validarUsuario

router = APIRouter(
    prefix="/emociones", tags=["Emociones"])

@router.get("/", response_model= EmocionesSalida)
async def consultarEmociones(request : Request, respuesta: UsuarioSelect= Depends(validarUsuario)) -> EmocionesSalida:
    emocionesDAO = EmocionesDAO(request.app.db)
    return emocionesDAO.consultaGeneral()