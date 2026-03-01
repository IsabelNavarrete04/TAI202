from fastapi import FastAPI, status, HTTPException
from typing import Literal
from pydantic import BaseModel, Field

app = FastAPI()

libros = []

class Libro(BaseModel):
    id: int = Field(..., gt=0, description="Identificador del libro")
    nombre: str = Field(...,  max_length=100, description="Nombre del libro")
    autor: str = Field(..., min_length=2, description="Nombre del autor")
    anio: int = Field(..., gt=1450, le=2025, description="Año de publicación, entre 1451 y 2026")
    paginas: int = Field(..., gt=1, description="Número de páginas que sea mayor a 1")
    estado: Literal["disponible", "prestado"] = Field("disponible", description="Estado del libro")

class Prestamo(BaseModel):
    id: int = Field(..., gt=0, description="Identificador del préstamo")
    IdLibro: int = Field(..., description="Identificador del libro a prestar")
    NombreUsuario: str = Field(..., min_length=2, max_length=50, description="Nombre del usuario")
    CorreoUsuario: str = Field(..., description="Correo del usuario")

#Registrar un libro
@app.post("/StayBooks/libros", status_code=status.HTTP_201_CREATED, tags=["Libros"])
async def registrar_libro(libro: Libro):
    if len(libro.nombre) < 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre del libro no es válido")
    
    libros.append(libro)

    return {
        "mensaje": "Libro registrado",
        "libro": libro
    }

#Listar todos los libros disponibles
@app.get("/StayBooks/libros", status_code=status.HTTP_200_OK, tags=["Libros"])
async def listar_libros():
    return {
        "mensaje": "Lista de libros disponibles",
        "libros": libros 
    }

#Buscar un libro por su nombre
@app.get("/StayBooks/libros/buscar", status_code=status.HTTP_200_OK, tags=["Libros"])
async def buscar_libro(nombre: str):
    if len(nombre) < 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre del libro no es válido")
    return {
        "mensaje": "Buscando libro con nombre: " + nombre
    }

#Registrar el préstamo de un libro a un usuario
@app.post("/StayBooks/prestamos", status_code=status.HTTP_201_CREATED, tags=["Préstamos"])
async def registrar_prestamo(prestamo: Prestamo):
    if prestamo.IdLibro == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El libro ya está prestado")
    return {
        "mensaje": "Préstamo registrado",
        "prestamo": prestamo
    }

#Marcar un libro como devuelto
@app.put("/StayBooks/prestamos/devolver/{IdPrestamo}", status_code=status.HTTP_200_OK, tags=["Préstamos"])
async def devolver_libro(IdPrestamo: int):
    if IdPrestamo <= 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El registro de préstamo no existe")
    return {
        "mensaje": "Libro del préstamo " + str(IdPrestamo) + " devuelto correctamente"
    }

#Eliminar el registro de un préstamo
@app.delete("/StayBooks/prestamos/{IdPrestamo}", status_code=status.HTTP_200_OK, tags=["Préstamos"])
async def eliminar_prestamo(IdPrestamo: int):
    if IdPrestamo <= 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El registro de préstamo no existe")
    return {
        "mensaje": "Préstamo " + str(IdPrestamo) + " eliminado correctamente"
    }