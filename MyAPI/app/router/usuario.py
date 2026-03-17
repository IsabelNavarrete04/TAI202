from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion


router = APIRouter(
    prefix = "/v1/usuarios", 
    tags = ["HTTP CRUD"]
)

@router.get("/")
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
    }

@router.post("/")
async def crear_usuario(usuario:crear_usuario):
    
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
 
    usuarios.append(usuario)
    
    return {
        "mensaje": "Usuario creado",
        "datos nuevos": usuario
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
