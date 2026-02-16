#importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional

#Instancoa del servidor
app = FastAPI()

usuarios=[
    {"id": 1, "nombre": "Fany", "edad": 21},
    {"id": 2, "nombre": "Aly", "edad": 21},
    {"id": 3, "nombre": "Dulce", "edad": 21}
]

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

@app.get("/v1/usuarios", tags=['HTTP CRUD'])
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
    }

@app.post("/v1/usuarios", tags=['HTTP CRUD'])
async def agregar_usuarios(usario:dict ):
    for usr in usuarios:
        if usr["id"] == usuarios.get("id"): 
            raise HTTPException(
                status_code= 400,
                detail= "El id ya existe"
            )
    usuarios.append(usuarios)
    return{
        "mensaje": "usuario creado",
        "datos nuevos": usuarios
    }