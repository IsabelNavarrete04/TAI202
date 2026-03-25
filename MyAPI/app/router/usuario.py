from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion
from sqlalchemy.orm import Session 
from app.data.db import get_db
from app.data.usuario import usuario as dbUusario 
from app.security.auth import verificar_peticion


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
async def actualizar_usuario(id: int, usuarioPut: dict, db: Session = Depends(get_db)):
    actualizarU = db.query(dbUusario).filter(dbUusario.id == id).first()
    
    if not actualizarU:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    actualizarU.nombre = usuarioPut.get("nombre")
    actualizarU.edad = usuarioPut.get("edad")
    db.commit()
    db.refresh(actualizarU)

    return {
        "mensaje": "usuario actualizado",
        "usuario": actualizarU
    }

@router.patch("/{id}")
async def modificar_usuario(id: int, datos: dict, db: Session = Depends(get_db)):
    modificarU = db.query(dbUusario).filter(dbUusario.id == id).first()
    if not modificarU:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    if "nombre" in datos:
            modificarU.nombre = datos["nombre"]

    if "edad" in datos:
            modificarU.edad = datos["edad"]  
    
    db.commit()
    db.refresh(modificarU)
        
    return {
            "mensaje": "usuario modificado",
            "usuario": modificarU
        }

@router.delete("/{id}")
async def eliminar_usuario(id: int, usuarioAuth:str = Depends(verificar_peticion), db: Session = Depends(get_db)):
    eliminarU = db.query(dbUusario).filter(dbUusario.id == id).first()
    if not eliminarU:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    db.delete(eliminarU)
    db.commit()

    return {
        "mensaje": f"Usuario eliminado por {usuarioAuth}",
        "usuario": eliminarU
    }
