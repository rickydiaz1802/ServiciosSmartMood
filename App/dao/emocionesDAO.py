from modelos.emocionesModel import EmocionesSalida
from modelos.usuariosModel import Salida
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

class EmocionesDAO:
    def __init__(self, db):
        self.db = db

    def consultaGeneral(self):
        salida = EmocionesSalida(mensaje = "", emociones=[])
        try:
            lista = list(self.db.EmocionesView.find())
            salida.mensaje = "Consulta exitosa. Listado de emociones:"
            salida.emociones = lista
        except Exception as ex:
            print(ex)
            salida.mensaje = "Error al hacer la consulta, tontito"
            salida.lista = None
        return salida