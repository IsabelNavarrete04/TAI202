from fastapi import FastAPI, status, HTTPException
from typing import Literal
from pydantic import BaseModel, Field
from datetime import datatime

app = FastAPI()

reservas =[]

class Reserva (BaseModel):
    nombre:str = Field(..., min_length=6, description="Nombre del usuario")
    fecha: datatime
    nPesonas: int = Field(..., ge= 1, gt=10, description="numero de personas entre 1 y 10")
    dia: str = Field(...,  min_length=1, max_digits=7, description="solo se captan en domingo")

@app.post("/reserva", status_code=status.HTTP_201_CREATED, tags=["rerservas"])
async def crear_reserva(reserva:Reserva):
    if len(reserva.nombre) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre no es válido")
    elif len(reserva.nPersonas) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El numero de personas no es válido")
    elif reserva.fecha == "8:00 AM" or "10:00 PM":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La hora debe ser entre 8:00 AM a 10:00 PM")
    elif reserva.

    reserva.append(reservas)

    return {
        "mensaje": "Libro registrado",
        "libro": libro
