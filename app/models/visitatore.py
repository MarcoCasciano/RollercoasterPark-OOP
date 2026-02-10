from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Visitatore(Base):
    __tablename__ = "visitatori"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cognome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # bambino, ragazzo, adulto
    posizione_x = Column(Integer, default=0)
    posizione_y = Column(Integer, default=0)
    
    # Relazione con Famiglia
    famiglia_id = Column(Integer, ForeignKey("famiglie.id"), nullable=True)
    famiglia = relationship("Famiglia", back_populates="visitatori")
    
    # Relazione con Giri
    giri = relationship("Giro", back_populates="visitatore")
