from fastapi import APIRouter, Request
from modelos.usuariosModel import UsuarioInsert, Salida, UsuariosSalida
from dao.usuariosDAO import UsuariosDAO

router = APIRouter(
    prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=Salida)
async def crearUsuario(usuario:UsuarioInsert, request: Request)->Salida:
    usuariosDAO = UsuariosDAO(request.app.db)
    return usuariosDAO.insertarUsuario(usuario)