from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Giro(Base):
    __tablename__ = "giri"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Chi ha fatto il giro
    visitatore_id = Column(Integer, ForeignKey("visitatori.id"), nullable=False)
    visitatore = relationship("Visitatore", back_populates="giri")
    
    # Su quale attrazione
    attrazione_id = Column(Integer, ForeignKey("attrazioni.id"), nullable=False)
    attrazione = relationship("Attrazione", back_populates="giri")
    
    # Quando è stato fatto
    timestamp = Column(DateTime, default=datetime.utcnow)
    ciclo = Column(Integer, default=0)  # numero del ciclo nella simulazione

