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
async def agregar_usuarios(usuario: dict):
    
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    
    usuarios.append(usuario)
    
    return {
        "mensaje": "Usuario creado",
        "datos nuevos": usuario
    }

@app.put("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario(id: int, usuario: dict):
    for i, usr in enumerate(usuarios):
        if usr["id"] == id:
            for j in usuarios:
                if j["id"] == usuario.get("id") and j["id"] != id:
                    raise HTTPException(
                        status_code=400,
                        detail="El id ya existe"
                    )
            usuarios[i] = usuario
            return {
                "mensaje": "usuario actualizado",
                "usuario": usuario
            }

@app.patch("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def modificar_usuario(id: int, datos: dict):
    for usuario in usuarios:
        if usuario["id"] == id:
            if "id" in datos:
                for i in usuarios:
                    if i["id"] == datos["id"] and i["id"] != id:
                        raise HTTPException(
                            status_code=400,
                            detail="el id ya existe"
                        )
            usuario.update(datos)
            return {
                "mensaje": "usuario modificado",
                "usuario": usuario
            }

@app.delete("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def eliminar_usuario(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {
                "mensaje": "Usuario eliminado",
                "usuario": usuario
            }
