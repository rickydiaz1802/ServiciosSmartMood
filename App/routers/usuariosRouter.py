from fastapi import APIRouter, Request
from modelos.usuariosModel import UsuarioInsert, CambiarDatos, Salida, UsuariosSalida, EliminarUsuario, CambiarContrasena
from dao.usuariosDAO import UsuariosDAO

router = APIRouter(
    prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=Salida)
async def crearUsuario(usuario:UsuarioInsert, request: Request)->Salida:
    usuariosDAO = UsuariosDAO(request.app.db)
    return usuariosDAO.insertarUsuario(usuario)

@router.delete("/{idUsuario}/eliminar", response_model=Salida)
async def eliminarUsuario(idUsuario: str, usuario: EliminarUsuario, request: Request)->Salida:
    usuariosDAO = UsuariosDAO(request.app.db)
    return usuariosDAO.eliminarUsuario(idUsuario, usuario)

@router.put("/{idUsuario}/cambiarcontrasena", response_model=Salida)
async def cambiarContrasena(idUsuario: str, contrasenas: CambiarContrasena, request: Request)->Salida:
    usuariosDAO = UsuariosDAO(request.app.db)
    return usuariosDAO.cambiarContrasena(idUsuario, contrasenas)

@router.put("/{idUsuario}/cambiardatos", response_model=Salida)
async def cambiarDatos(idUsuario: str, datos: CambiarDatos, request: Request)->Salida:
    usuariosDAO = UsuariosDAO(request.app.db)
    return usuariosDAO.cambiarDatos(idUsuario, datos)

@router.get("/", response_model=UsuariosSalida)
async def consultarUsuarios(request : Request) -> UsuariosSalida:
    usuariosDAO = UsuariosDAO(request.app.db)
    return usuariosDAO.consultaGeneral()