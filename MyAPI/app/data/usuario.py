from sqlalchemy import Column, Interger, String
from app.data.db import Base

class usuario(Base):
    __tablename__ = "tb-usuarios"
    
    id = Column(Interger, primary_key = True, index = True)
    nombre = Column(String)
    edad = Column(Interger)