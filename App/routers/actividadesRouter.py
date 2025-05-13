from fastapi import APIRouter, Request
from modelos.usuariosModel import Salida
from modelos.actividadesModel import ActividadInsert, ActividadesSalida, EliminarActividad, CambiarDatosActividad
from dao.actividadesDAO import ActividadesDAO

router = APIRouter(
    prefix="/actividades", tags=["Actividades"])

@router.post("/", response_model=Salida)
async def crearActividad(actividad:ActividadInsert, request: Request)->Salida:
    actividadesDAO = ActividadesDAO(request.app.db)
    return actividadesDAO.insertarActividad(actividad)

@router.delete("/{idActividad}/eliminar", response_model=Salida)
async def eliminarActividad(idActividad: str, actividad: EliminarActividad, request: Request)->Salida:
    actividadesDAO = ActividadesDAO(request.app.db)
    return actividadesDAO.eliminarActividad(idActividad, actividad)

@router.put("/{idActividad}/cambiardatos", response_model=Salida)
async def cambiarDatos(idActividad: str, datos: CambiarDatosActividad, request: Request)->Salida:
    actividadesDAO = ActividadesDAO(request.app.db)
    return actividadesDAO.cambiarDatos(idActividad, datos)

@router.get("/", response_model=ActividadesSalida)
async def consultarActividades(request : Request) -> ActividadesSalida:
    actividadesDAO = ActividadesDAO(request.app.db)
    return actividadesDAO.consultaGeneral()

@router.get("/{idUsuario}", response_model=ActividadesSalida)
async def consultarActividadesDelUsuario(idUsuario:str,request : Request) -> ActividadesSalida:
    actividadesDAO = ActividadesDAO(request.app.db)
    return actividadesDAO.consultaActividadesDelUsuario(idUsuario)