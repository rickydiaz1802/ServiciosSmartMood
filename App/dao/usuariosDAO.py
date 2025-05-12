from modelos.usuariosModel import UsuarioInsert, Salida, UsuariosSalida
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
