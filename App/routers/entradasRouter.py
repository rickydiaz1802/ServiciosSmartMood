from fastapi import APIRouter, Request, Depends
from modelos.usuariosModel import Salida
from modelos.entradasModel import EntradaInsert, EntradaCompleta, EntradaSelect, CambiarDatosEntrada, EntradasSalida
from routers.usuariosRouter import validarUsuario
from modelos.usuariosModel import UsuarioSelect
from dao.entradasDAO import EntradasDAO

router = APIRouter(
    prefix="/entradas", tags=["Entradas"])

@router.post("/", response_model=Salida)
async def crearEntrada(entrada:EntradaInsert, request: Request, respuesta: UsuarioSelect= Depends(validarUsuario))->Salida:
    salida = Salida(mensaje="")
    idUsuario = str(respuesta["_id"])
    print(respuesta)
    if respuesta and respuesta["tipo"] in ("administrador", "usuario"):
        entradasDAO = EntradasDAO(request.app.db)
        return entradasDAO.insertarEntrada(idUsuario, entrada)
    else:
        salida.mensaje = "Error. Usuario no encontrado o sin permisos"
        return salida

@router.delete("/eliminar/{idEntrada}", response_model=Salida)
async def eliminarEntrada( idEntrada: str, request: Request, respuesta: UsuarioSelect= Depends(validarUsuario))->Salida:
    salida = Salida(mensaje="")
    contrasena = respuesta["contrasena"]
    print(respuesta)
    if respuesta and respuesta["tipo"] in ("administrador", "usuario"):
        entradasDAO = EntradasDAO(request.app.db)
        return entradasDAO.eliminarEntrada(idEntrada, contrasena)
    else:
        salida.mensaje = "Error. Usuario no encontrado o sin permisos"
        return salida

@router.put("/{idEntrada}/cambiardatos", response_model=Salida)
async def cambiarDatos(idEntrada: str, datos: CambiarDatosEntrada, request: Request, respuesta: UsuarioSelect= Depends(validarUsuario))->Salida:
    salida = Salida(mensaje="")
    contrasena = respuesta["contrasena"]
    print(respuesta)
    if respuesta and respuesta["tipo"] in ("administrador", "usuario"):
        entradasDAO = EntradasDAO(request.app.db)
        return entradasDAO.cambiarDatos(idEntrada, contrasena, datos)
    else:
        salida.mensaje = "Error. Usuario no encontrado o sin permisos"
        return salida

@router.get("/", response_model=EntradasSalida)
async def consultarEntradas(request : Request, respuesta: UsuarioSelect= Depends(validarUsuario)) -> EntradasSalida:
    print(respuesta)
    if respuesta and respuesta["tipo"] == "administrador":
        entradasDAO = EntradasDAO(request.app.db)
        return entradasDAO.consultaGeneral()
    else:
        return EntradasSalida(entradas=[], mensaje="Error. Usuario no encontrado o sin permisos")

@router.get("/{idUsuario}", response_model=EntradasSalida)
async def consultarEntradasDelUsuario(idUsuario:str,request : Request, respuesta: UsuarioSelect= Depends(validarUsuario)) -> EntradasSalida:
    print(respuesta)
    if respuesta and respuesta["tipo"] in ("administrador", "usuario"):
        entradasDAO = EntradasDAO(request.app.db)
        return entradasDAO.consultaUsuario(idUsuario)
    else:
        return EntradasSalida(entradas=[], mensaje="Error. Usuario no encontrado o sin permisos")

@router.get("/{idEntrada}", response_model=EntradasSalida)
async def consultarEntradaIndividual(idEntrada:str,request : Request, respuesta: UsuarioSelect= Depends(validarUsuario)) -> EntradasSalida:
    print(respuesta)
    if respuesta and respuesta["tipo"] in ("administrador", "usuario"):
        entradasDAO = EntradasDAO(request.app.db)
        return entradasDAO.consultaPorId(idEntrada)
    else:
        return EntradasSalida(entradas=[], mensaje="Error. Usuario no encontrado o sin permisos")



