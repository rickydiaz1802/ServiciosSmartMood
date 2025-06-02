from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from modelos.entradasModel import EntradaInsert, EntradaCompleta, EntradaSelect, CambiarDatosEntrada, EntradasSalida
from modelos.usuariosModel import Salida
from dao.usuariosDAO import UsuariosDAO

class EntradasDAO:
    def __init__(self, db):
        self.db = db

    def insertarEntrada(self,  usuarioId: str, entradaInsert: EntradaInsert):
        salida = Salida(mensaje="")
        entrada = EntradaCompleta(idUsuario=usuarioId, nota=entradaInsert.nota, emocionesNumeros= entradaInsert.emocionesNumeros,
                                  actividad=entradaInsert.actividad, fecha=entradaInsert.fecha)
        try:
            usuarioDao = UsuariosDAO(self.db)
            usuario = usuarioDao.verificarUsuario(entrada.idUsuario)
            if usuario:
                result = self.db.Entradas.insert_one(jsonable_encoder(entrada))
                salida.mensaje = "Entrada insertada con exito"
            else:
                salida.mensaje = "Error. Usuario no encontrado."
        except Exception as ex:
            print(ex)
            salida.mensaje = "Algo salió mal y no sé que"
        return salida

    def verificarEntrada(self, idEntrada:str):
        entrada = None
        try:
            entrada = self.db.Entradas.find_one({"_id": ObjectId(idEntrada), "eliminada": {"$exists": False}})
        except Exception as ex:
            print(ex)
        return entrada

    def eliminarEntrada(self, idEntrada: str, contrasena: str):
        salida = Salida(mensaje="")
        try:
            entradaRegistrada = self.verificarEntrada(idEntrada)
            if entradaRegistrada:
                usuarioDao = UsuariosDAO(self.db)
                usuario = usuarioDao.verificarUsuario(entradaRegistrada["idUsuario"])
                if usuario:
                    if contrasena == usuario["contrasena"]:
                        self.db.Entradas.update_one({"_id": ObjectId(idEntrada)}, {"$set": {"eliminada": True}})
                        salida.mensaje ="Entrada eliminada con éxito."
                    else:
                         salida.mensaje = "Error. Contraseña incorrecta."
                else:
                    salida.mensaje = "Error. Usuario no encontrado"
            else:
                salida.mensaje = "Error. La actividad no fue encontrada."
        except Exception as ex:
            print(ex)
            salida.mensaje = "Algo salió mal y no sé que"
        return salida

    def cambiarDatos(self, idEntrada:str, contrasena:str, datos: CambiarDatosEntrada):
        salida = Salida(mensaje="")
        try:
            entrada = self.verificarEntrada(idEntrada)
            if entrada:
                usuarioDao = UsuariosDAO(self.db)
                usuario = usuarioDao.verificarUsuario(entrada["idUsuario"])
                if usuario:
                    if contrasena == usuario["contrasena"]:
                        cambios = {}
                        if datos.nota is not None and datos.nota != "":
                            cambios["nota"] = datos.nota
                        if datos.emocionesNumeros is not None and datos.emocionesNumeros != "":
                            cambios["emocionesNumeros"] = datos.emocionesNumeros
                        if datos.actividad is not None and datos.actividad != "":
                            cambios["actividad"] = datos.actividad
                        if datos.fecha is not None and datos.fecha != "":
                            cambios["fecha"] = datos.fecha
                        if cambios:
                            self.db.Actividades.update_one({"_id" : ObjectId(idEntrada)}, {"$set": cambios})
                            salida.mensaje = "Datos cambiados con éxito."
                        else:
                            salida.mensaje = "Error. No se introdujeron nuevos datos."
                    else:
                        salida.mensaje = "Error. Contraseña incorrecta."
                else:
                    salida.mensaje = "Error. Usuario no encontrado."
            else:
                salida.mensaje = "Error. Entrada no encontrada."
        except Exception as ex:
            print(ex)
            salida.mensaje = "Error. Algo salió mal y no sé que fue"
        return salida

    def consultaGeneral(self):
        salida = EntradasSalida(mensaje = "", entradas=[])
        try:
            lista = list(self.db.EntradasView.find({"eliminada": {"$exists": False}}))
            salida.mensaje = "Consulta exitosa. Listado de entradas:"
            salida.actividades = lista
        except Exception as ex:
            print(ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al hacer la consulta, tontito"
            salida.lista = None
        return salida

    def consultaUsuario(self, idUsuario:str):
        salida = EntradasSalida(mensaje = "", entradas=[])
        try:
            lista = list(self.db.EntradasView.find({"eliminada": {"$exists": False}}))
            salida.mensaje = "Consulta exitosa. Listado de entradas:"
            salida.actividades = lista
        except Exception as ex:
            print(ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al hacer la consulta, tontito"
            salida.lista = None
        return salida

