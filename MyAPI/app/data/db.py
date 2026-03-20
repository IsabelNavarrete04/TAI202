from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base
import os 

#definimos la URL de conexión
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@postgres:5432/DB_miapi"
)

#creamos el motor de la conexión 
engine = create_engine(DATABASE_URL)

#preparamos el gestionador de sesiones 
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine 
)

#base declarativa del modelo
Base = declarative_base()

#obtener sesiones de cada petición 
def get_db():
    db = SessionLocal()
    try:
        yield db  #yield: mandar o imprimir lo que tenga db
    finally:
        db.close()