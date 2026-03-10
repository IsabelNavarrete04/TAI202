from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI()

reservas =[]

class Reserva (BaseModel):
    id: int = Field(..., gt=0, description="Identificador de la reserva")
    nombre:str = Field(..., min_length=6, description="Nombre del usuario")
    fecha: datetime
    nPesonas: int = Field(..., ge= 1, gt=9, description="numero de personas entre 1 y 10")
    dia: str = Field(...,  min_length=1, max_digits=7, description="solo se captan en domingo")
 
security = HTTPBasic()

def verificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuario_correcto = secrets.compare_digest(credentials.username, "admin")
    contrasena_correcta = secrets.compare_digest(credentials.password, "rest123")

    if not(usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = " Credenciales no válidas"
        )
    return credentials.username 

@app.post("/reserva", status_code=status.HTTP_201_CREATED, tags=["rerservas"])
async def crear_reserva(reserva:Reserva):
    if len(reserva.nombre) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre no es válido")
    elif len(reserva.nPersonas) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El numero de personas no es válido")
    elif reserva.fecha == "8:00 AM" or "10:00 PM":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La hora debe ser entre 8:00 AM a 10:00 PM")
    elif reserva.dia == "domingo":
        raise HTTPException(status_code=status.HTTP_200_OK)

    reserva.append(reservas)

    return {
        "mensaje": "Reserva Creada",
        "libro": reserva
    }

@app.get("/listar", status_code=status.HTTP_200_OK, tags=["reservas"])
async def listar_reservas(usuarioAuth:str = Depends(verificar_peticion)):
    return {
        "mensaje": "Lista de reservas disponibles",
        "libros": reservas
    }


@app.get("/buscar/{id}", status_code=status.HTTP_200_OK, tags=["reservas"])
async def buscar_reserva(id:int, reserva:Reserva):
    if reserva.id == id :
        return {
            "mensaje": "Buscando reserrva con id: " + id
        }
