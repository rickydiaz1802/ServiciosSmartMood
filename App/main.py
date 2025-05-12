from dao.database import Conexion
from routers import actividadesRouter, emocionesRouter, entradasRouter, usuariosRouter
import uvicorn
from fastapi import FastAPI

app = FastAPI()
app.include_router(actividadesRouter.router)
app.include_router(emocionesRouter.router)
app.include_router(entradasRouter.router)
app.include_router(usuariosRouter.router)
@app.get("/")
async def home():
    salida = {"Bienvenido de vuelta señor Stark"}
    return salida

@app.on_event("startup")
async def startup():
    print("Conectando con MongoDB")
    conexion = Conexion()
    app.conexion=conexion
    app.db=conexion.getDB()

@app.on_event("shutdown")
async def shutdown():
    print("Cerrando la conexion con MongoDB")
    app.conexion.cerrar()



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", reload=True)