from modelos.actividadesModel import ActividadesSalida, ActividadInsert, EliminarActividad, CambiarDatosActividad
from modelos.usuariosModel import Salida
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from dao.usuariosDAO import UsuariosDAO

class ActividadesDAO:
    def __init__(self, db):
        self.db = db

    def insertarActividad(self, actividad: ActividadInsert):
        salida = Salida(mensaje="")
        try:
            usuarioDao = UsuariosDAO(self.db)
            usuario = usuarioDao.verificarUsuario(actividad.idUsuario)
            if usuario:
                result = self.db.Actividades.insert_one(jsonable_encoder(actividad))
                salida.mensaje = "Actividad insertada con exito"
            else:
                salida.mensaje = "Error. Usuario no encontrado."
        except Exception as ex:
            print(ex)
            salida.mensaje = "Algo salió mal y no sé que"
        return salida

    def verificarActividad(self, idActividad:str):
        actividad = None
        try:
            actividad = self.db.Actividades.find_one({"_id": ObjectId(idActividad)})
        except Exception as ex:
            print(ex)
        return actividad

    def eliminarActividad(self, idActividad: str, actividad:EliminarActividad):
        salida = Salida(mensaje="")
        try:
            actividadRegistrada = self.verificarActividad(idActividad)
            if actividadRegistrada:
                usuarioDao = UsuariosDAO(self.db)
                usuario = usuarioDao.verificarUsuario(actividadRegistrada["idUsuario"])
                if usuario:
                    if actividad.contrasena == usuario["contrasena"]:
                        self.db.Actividades.delete_one({"_id": ObjectId(idActividad)})
                        salida.mensaje ="Actividad eliminada con éxito."
                    else:
                         salida.mensaje = "Error. Contraseña incorrecta."
                else:
                    salida.mensaje = ""
            else:
                salida.mensaje = "Error. La actividad no fue encontrada."
        except Exception as ex:
            print(ex)
            salida.mensaje = "Algo salió mal y no sé que"
        return salida

    def cambiarDatos(self, idActividad:str, datos: CambiarDatosActividad):
        salida = Salida(mensaje="")
        try:
            actividad = self.verificarActividad(idActividad)
            if actividad:
                cambios = {}
                if datos.nombre is not None and datos.nombre != "":
                    cambios["nombre"] = datos.nombre
                if datos.descripcion is not None and datos.descripcion != "":
                    cambios["descripcion"] = datos.descripcion
                if datos.icono is not None and datos.icono != "":
                    cambios["icono"] = datos.icono
                if cambios:
                    self.db.Actividades.update_one({"_id" : ObjectId(idActividad)}, {"$set": cambios})
                    salida.mensaje = "Datos cambiados con éxito."
                else:
                    salida.mensaje = "Error. No se introdujeron nuevos datos."
            else:
                salida.mensaje = "Error. Actividad no encontrada."
        except Exception as ex:
            print(ex)
            salida.mensaje = "Error. Algo salió mal y no sé que fue"
        return salida

    def consultaGeneral(self):
        salida = ActividadesSalida(mensaje = "", actividades=[])
        try:
            lista = list(self.db.ActividadesView.find())
            salida.mensaje = "Consulta exitosa. Listado de actividades:"
            salida.actividades = lista
        except Exception as ex:
            print(ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al hacer la consulta, tontito"
            salida.lista = None
        return salida

    def consultaActividadesDelUsuario(self, idUsuario:str):
        salida = ActividadesSalida(mensaje = "", actividades=[])
        try:
            usuarioDao = UsuariosDAO(self.db)
            usuario = usuarioDao.verificarUsuario(idUsuario)
            if usuario:
                lista = list(self.db.ActividadesView.find({"idUsuario" : idUsuario}))
                salida.mensaje = "Consulta exitosa. Listado de actividades:"
                salida.actividades = lista
            else:
                salida.mensaje = "Error. Usuario no encontrado."
        except Exception as ex:
            print(ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al hacer la consulta, tontito"
            salida.lista = None
        return salida