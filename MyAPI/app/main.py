#importaciones
from fastapi import FastAPI
from app.router import usuario, misc
from app.data.db import engine
from app.data import usuario as usuarioDB

usuarioDB.Base.metadata.create_all(bind = engine)

#Instancoa del servidor
app = FastAPI()

app.include_router(usuario.router)
app.include_router(misc.misc)

