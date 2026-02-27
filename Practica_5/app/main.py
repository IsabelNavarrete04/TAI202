from fastapi import FastAPI, status, HTTPException
from typing import Literal
from pydantic import BaseModel, Field

app = FastAPI()

class libros (BaseModel):
    nombre:str = Field(..., min_length=2, max_digits=100)
    autor:str = Field(..., min_length=2, max_digits=100)
    anio_publicacion: int = Field(..., gt=1450)
    status: Literal["disponible", "prestado"] = "disponible"
    paginas: int = Field(..., gt=1)

class prestamos(BaseModel):
    IdLibro:int = Field(..., gt=1)
    NombreUsuario: str = Field(..., min_length=2, max_digits=100)
    CorreoUsuario: str = Field(..., min_length=8, max_digits=50)

@app.post("/staybook/libros/", status_code=201)
def regristrar_libro(libro:libros):
    nuevoLibro = libro
