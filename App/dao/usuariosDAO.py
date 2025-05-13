from modelos.usuariosModel import UsuarioInsert, UsuariosSalida, CambiarDatos, Salida, UsuariosSalida, EliminarUsuario, CambiarContrasena
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

class UsuariosDAO:
    def __init__(self, db):
        self.db = db

    def verificarContrasenaSeguridad(self, contrasena):
        salida = Salida(mensaje="")
        respuesta = False
        try:
            if len(contrasena) > 4:
                if any(c.isalpha() for c in contrasena):
                    if any(not c.isalpha() for c in contrasena):
                        respuesta = True
                    else:
                        respuesta = False
                        salida.mensaje = "Error. La contraseña no contiene simbolos no alfabéticos"
                else:
                    respuesta = False
                    salida.mensaje = "Error. La contraseña no contiene letras"
            else:
                respuesta = False
                salida.mensaje = "Error. La contraseña es muy corta. Debe tener 5 caracteres o más."
        except Exception as ex:
            print(ex)
            salida.mensaje = "Error al verificar la contraseña"
        return respuesta, salida

    def insertarUsuario(self, usuario: UsuarioInsert):
        salida = Salida(mensaje="")
        try:
            verificarContrasena, salidaVerificacion = self.verificarContrasenaSeguridad(usuario.contrasena)
            if verificarContrasena:
                if usuario.correo.endswith(("@gmail.com", "@accitesz.com")):
                    if usuario.edad >= 2:
                        result = self.db.Usuarios.insert_one(jsonable_encoder(usuario))
                        salida.mensaje = "Usuario insertado con exito"
                    else:
                        salida.mensaje = "Error. El usuario no tiene la edad suficiente"
                else:
                    salida.mensaje = "Error. Dirección de correo no válida. Asegurese de que pertenezca a uno de los siguientes dominios: @gmail.com, @accitesz.com"
            else:
                salida = salidaVerificacion
        except Exception as ex:
            print(ex)
            salida.mensaje = "Algo salió mal y no sé que"
        return salida

    def verificarUsuario(self, idusuario:str):
        usuario = None
        try:
            usuario = self.db.Usuarios.find_one({"_id": ObjectId(idusuario)})
        except Exception as ex:
            print(ex)
        return usuario

    def eliminarUsuario(self, idUsuario: str, usuario:EliminarUsuario):
        salida = Salida(mensaje="")
        try:
            usuarioRegistrado = self.verificarUsuario(idUsuario)
            if usuarioRegistrado:
                if usuario.contrasena == usuarioRegistrado["contrasena"]:
                    self.db.Usuarios.delete_one({"_id": ObjectId(idUsuario)})
                    salida.mensaje = "Usuario eliminado con exito"
                else:
                    salida.mensaje = "Error. Contraseña incorrecta"
            else:
                salida.mensaje = "Error. Usuario no encontrado."
        except Exception as ex:
            print(ex)
            salida.mensaje = "Algo salió mal y no sé que"
        return salida

    def cambiarContrasena(self, idUsuario:str, contrasenas: CambiarContrasena):
        salida = Salida(mensaje="")
        try:
            usuarioRegistrado = self.verificarUsuario(idUsuario)
            if usuarioRegistrado:
                if contrasenas.contrasenaAnterior == usuarioRegistrado["contrasena"]:
                    verificarContrasena, salidaVerificacion = self.verificarContrasenaSeguridad(contrasenas.contrasenaNueva)
                    if verificarContrasena:
                        self.db.Usuarios.update_one({"_id": ObjectId(idUsuario)},{"$set":{"contrasena": contrasenas.contrasenaNueva}})
                        salida.mensaje="Contraseña actualizada con éxito."
                    else:
                        salida = salidaVerificacion
                else:
                    salida.mensaje = "Error. Contraseña anterior incorrecta."
            else:
                salida.mensaje = "Error. Usuario no encontrado."
        except Exception as ex:
            print(ex)
            salida.mensaje = "Error. Algo salió mal y no sé que fue"
        return salida

    def cambiarDatos(self, idUsuario:str, datos: CambiarDatos):
        salida = Salida(mensaje="")
        try:
            usuario = self.verificarUsuario(idUsuario)
            if usuario:
                if datos.contrasena == usuario["contrasena"]:
                    cambios = {}
                    if datos.nombre is not None:
                        cambios["nombre"] = datos.nombre
                    if datos.correo is not None:
                        if datos.correo.endswith(("@gmail.com", "@accitesz.com")):
                            cambios["correo"] = datos.correo
                    if datos.edad is not None:
                        if datos.edad >= 2:
                            cambios["edad"] = datos.edad
                    if cambios:
                        self.db.Usuarios.update_one({"_id" : ObjectId(idUsuario)}, {"$set": cambios})
                        salida.mensaje = "Datos cambiados con éxito."
                    else:
                        salida.mensaje = "Error. No se introdujeron nuevos datos."
                else:
                    salida.mensaje = "Error. Contraseña incorrecta."
            else:
                salida.mensaje = "Error. Usuario no encontrado."
        except Exception as ex:
            print(ex)
            salida.mensaje = "Error. Algo salió mal y no sé que fue"
        return salida

    def consultaGeneral(self):
        salida = UsuariosSalida(mensaje = "", usuarios=[])
        try:
            lista = list(self.db.UsuariosView.find())
            salida.mensaje = "Consulta exitosa. Listado de usuarios:"
            salida.usuarios = lista
        except Exception as ex:
            print(ex)
            salida.estatus = "ERROR"
            salida.mensaje = "Error al hacer la consulta, tontito"
            salida.lista = None
        return salida








