from fastapi import APIRouter, Request
from dao.emocionesDAO import EmocionesDAO
from modelos.emocionesModel import EmocionesSalida

router = APIRouter(
    prefix="/emociones", tags=["Emociones"])

@router.get("/", response_model= EmocionesSalida)
async def consultarEmociones(request : Request) -> EmocionesSalida:
    emocionesDAO = EmocionesDAO(request.app.db)
    return emocionesDAO.consultaGeneral()