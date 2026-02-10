from sqlalchemy import Column, Integer, String, Boolean, Float
from app.db.database import Base

class Attrazione(Base):
    __tablename__ = "attrazioni"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True, nullable=False)
    per_bambini = Column(Boolean, default=True)
    capienza_massima = Column(Integer, default=5)
    durata_giro = Column(Integer, default=2)
    posizione_x = Column(Float, default=0.0)
    posizione_y = Column(Float, default=0.0)
