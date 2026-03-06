#importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "Isabel_Practica_siete"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2 = OAuth2PasswordBearer(tokenUrl="token")

#Instancoa del servidor
app = FastAPI()

usuarios=[
    {"id": 1, "nombre": "Fany", "edad": 21},
    {"id": 2, "nombre": "Aly", "edad": 21},
    {"id": 3, "nombre": "Dulce", "edad": 21}
]

class crear_usuario(BaseModel):
    id:int = Field(...,gt=0, description="Identificador de usuario")
    nombre:str = Field(...,min_length=3,max_length=50, example="Isabel")
    edad:int = Field(...,ge=1,le=123, description="Edad valida entre 1 y 123")

def crear_token(data: dict):
    datos = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos.update({"exp": expiracion})
    token = jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verificar_token(token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")

        if usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return usuario

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )


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

@app.put("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario(id: int, usuario: dict, user: str = Depends(verificar_token)):
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
                "mensaje": f"Usuario actualizado por {user}",
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

@app.delete("/v1/usuarios/{id}")
async def eliminar_usuario(id: int, user: str = Depends(verificar_token)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {
                "mensaje": f"Usuario eliminado por {user}",
                "usuario": usuario
            }

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    if form_data.username != "IsabelNavarrete" or form_data.password != "123456":
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    token = crear_token({"sub": form_data.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }