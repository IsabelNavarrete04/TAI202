import asyncio
from typing import Optional
from fastapi import APIRouter

misc = APIRouter(
    tags = ["Varios"]
)

#Endpoints
@misc.get("/") #-----> arranque
async def holamundo():
    return {"mensaje":"Hola mundo FastAPI"}

@misc.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje": "Bienvenido a FastAPI",
        "estatus": "200",
    }

@misc.get("/stay")
async def stay(stay: str):
    return {"mensaje": f"Hola {stay}!"}

@misc.get("/Straykids")
async def StrayKids(message: Optional[str] = None):
    if message:
        return {"mensaje": message}
    return {"mensaje": "STRAY KIDS EVERYWHERE ALL AROUND THE WORLD"}
