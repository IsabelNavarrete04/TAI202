from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion
from sqlalchemy.orm import Session 
from app.data.db import get_db
from app.data.usuario import usuario as dbUusario 


router = APIRouter(
    prefix = "/v1/usuarios", 
    tags = ["HTTP CRUD"]
)

@router.get("/")
async def leer_usuarios(db:Session = Depends(get_db)):

    queryUsuarios = db.query(dbUusario).all()
    
    return {
        "total": len(queryUsuarios),
        "usuarios": queryUsuarios,
        "status": "200"
    }

@router.post("/")
async def crear_usuario(usuarioP:crear_usuario, db:Session = Depends(get_db)):
    
    nuevoU = dbUusario(nombre = usuarioP.nombre, edad = usuarioP.edad)
    db.add(nuevoU)
    db.commit()
    db.refresh(nuevoU)

    return {
        "mensaje": "Usuario creado",
        "datos nuevos": nuevoU
    }

@router.put("/{id}")
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

@router.patch("/{id}")
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

@router.delete("/{id}")
async def eliminar_usuario(id: int, usuarioAuth:str = Depends(verificar_peticion)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {
                "mensaje": f"Usuario eliminado por {usuarioAuth}",
                "usuario": usuario
            }
