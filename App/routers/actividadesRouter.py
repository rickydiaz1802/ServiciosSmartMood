from fastapi import APIRouter, Request, Depends
from modelos.usuariosModel import Salida
from modelos.actividadesModel import ActividadInsert, ActividadesSalida, EliminarActividad, CambiarDatosActividad
from dao.actividadesDAO import ActividadesDAO
from routers.usuariosRouter import validarUsuario
from modelos.usuariosModel import UsuarioSelect

router = APIRouter(
    prefix="/actividades", tags=["Actividades"])

@router.post("/", response_model=Salida)
async def crearActividad(actividad:ActividadInsert, request: Request, respuesta: UsuarioSelect= Depends(validarUsuario))->Salida:
    salida = Salida(mensaje="")
    print(respuesta)
    if respuesta and respuesta["tipo"] in ("administrador", "usuario"):
        actividadesDAO = ActividadesDAO(request.app.db)
        return actividadesDAO.insertarActividad(actividad)
    else:
        salida.mensaje = "Error. Usuario no encontrado o sin permisos"
        return salida

@router.delete("/{idActividad}/eliminar", response_model=Salida)
async def eliminarActividad(idActividad: str, actividad: EliminarActividad, request: Request, respuesta: UsuarioSelect= Depends(validarUsuario))->Salida:
    salida = Salida(mensaje="")
    print(respuesta)
    if respuesta and respuesta["tipo"] in ("administrador", "usuario"):
        actividadesDAO = ActividadesDAO(request.app.db)
        return actividadesDAO.eliminarActividad(idActividad, actividad)
    else:
        salida.mensaje = "Error. Usuario no encontrado o sin permisos"
        return salida

@router.put("/{idActividad}/cambiardatos", response_model=Salida)
async def cambiarDatos(idActividad: str, datos: CambiarDatosActividad, request: Request, respuesta: UsuarioSelect= Depends(validarUsuario))->Salida:
    salida = Salida(mensaje="")
    print(respuesta)
    if respuesta and respuesta["tipo"] in ("administrador", "usuario"):
        actividadesDAO = ActividadesDAO(request.app.db)
        return actividadesDAO.cambiarDatos(idActividad, datos)
    else:
        salida.mensaje = "Error. Usuario no encontrado o sin permisos"
        return salida

@router.get("/", response_model=ActividadesSalida)
async def consultarActividades(request : Request, respuesta: UsuarioSelect= Depends(validarUsuario)) -> ActividadesSalida:

    print(respuesta)
    if respuesta and respuesta["tipo"] == "administrador":
        actividadesDAO = ActividadesDAO(request.app.db)
        return actividadesDAO.consultaGeneral()
    else:
        return ActividadesSalida(actividades=[], mensaje="Error. Usuario no encontrado o sin permisos")

@router.get("/{idUsuario}", response_model=ActividadesSalida)
async def consultarActividadesDelUsuario(idUsuario:str,request : Request, respuesta: UsuarioSelect= Depends(validarUsuario)) -> ActividadesSalida:
    print(respuesta)
    if respuesta and respuesta["tipo"] in ("administrador", "usuario"):
        actividadesDAO = ActividadesDAO(request.app.db)
        return actividadesDAO.consultaActividadesDelUsuario(idUsuario)
    else:
        return ActividadesSalida(actividades=[], mensaje="Error. Usuario no encontrado o sin permisos")