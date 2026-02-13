#importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional

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

@app.get("/stay")
async def stay(stay: str):
    return {"mensaje": f"Hola {stay}!"}

@app.get("/Straykids")
async def StrayKids(message: Optional[str] = None):
    if message:
        return {"mensaje": message}
    return {"mensaje": "STRAY KIDS EVERYWHERE ALL AROUND THE WORLD"}