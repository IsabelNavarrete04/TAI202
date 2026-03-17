#importaciones
from fastapi import FastAPI
from app.router import usuario, misc

#Instancoa del servidor
app = FastAPI()

app.include_router(usuario.router)
app.include_router(misc.misc)