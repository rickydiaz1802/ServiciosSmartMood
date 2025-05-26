from fastapi import APIRouter, Request, Depends
from modelos.usuariosModel import UsuarioInsert, CambiarDatos, UsuarioSelect, Salida, UsuariosSalida, EliminarUsuario, CambiarContrasena
from dao.usuariosDAO import UsuariosDAO
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(
    prefix="/usuarios", tags=["Usuarios"])
security = HTTPBasic()

async def validarUsuario(request:Request, credenciales:HTTPBasicCredentials = Depends(security))->UsuarioSelect:
    usuarioDAO = UsuariosDAO(request.app.db)
    return usuarioDAO.verificarUsuarioConCorreo(credenciales.username, credenciales.password)

@router.post("/", response_model=Salida)
async def crearUsuario(usuario:UsuarioInsert, request: Request)->Salida:
    usuariosDAO = UsuariosDAO(request.app.db)
    return usuariosDAO.insertarUsuario(usuario)

@router.delete("/{idUsuario}/eliminar", response_model=Salida)
async def eliminarUsuario(idUsuario: str, usuario: EliminarUsuario, request: Request, respuesta: UsuarioSelect= Depends(validarUsuario))->Salida:
    salida = Salida(mensaje = "")
    print(respuesta)
    if respuesta and respuesta["tipo"] in ("administrador", "usuario"):
        usuariosDAO = UsuariosDAO(request.app.db)
        return usuariosDAO.eliminarUsuario(idUsuario, usuario)
    else:
        salida.mensaje = "Error. Usuario no encontrado o sin permisos"
        return salida

@router.put("/{idUsuario}/cambiarcontrasena", response_model=Salida)
async def cambiarContrasena(idUsuario: str, contrasenas: CambiarContrasena, request: Request, respuesta: UsuarioSelect= Depends(validarUsuario))->Salida:
    salida = Salida(mensaje="")
    print(respuesta)
    if respuesta and respuesta["tipo"] in ("administrador", "usuario"):
        usuariosDAO = UsuariosDAO(request.app.db)
        return usuariosDAO.cambiarContrasena(idUsuario, contrasenas)
    else:
        salida.mensaje = "Error. Usuario no encontrado o sin permisos"
        return salida

@router.put("/{idUsuario}/cambiardatos", response_model=Salida)
async def cambiarDatos(idUsuario: str, datos: CambiarDatos, request: Request, respuesta: UsuarioSelect= Depends(validarUsuario))->Salida:
    salida = Salida(mensaje="")
    print(respuesta)
    if respuesta and respuesta["tipo"] in ("administrador", "usuario"):
        usuariosDAO = UsuariosDAO(request.app.db)
        return usuariosDAO.cambiarDatos(idUsuario, datos)
    else:
        salida.mensaje = "Error. Usuario no encontrado o sin permisos"
        return salida

@router.get("/", response_model=UsuariosSalida)
async def consultarUsuarios(request : Request, respuesta: UsuarioSelect= Depends(validarUsuario)) -> UsuariosSalida:

    print(respuesta)
    if respuesta and respuesta["tipo"] == "administrador":
        usuariosDAO = UsuariosDAO(request.app.db)
        return usuariosDAO.consultaGeneral()
    else:
        return UsuariosSalida(usuarios=[], mensaje="Error. Usuario no encontrado o sin permisos")
