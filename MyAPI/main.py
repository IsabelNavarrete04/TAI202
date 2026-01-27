#importaciones
from fastapi import FastAPI
import asyncio

#Instancoa del servidor
app = FastAPI()

#Endpoints
@app.get("/") #-----> arranque
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje": "Bienvenido a FastAPI",
        "estatus": "200",
    }