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