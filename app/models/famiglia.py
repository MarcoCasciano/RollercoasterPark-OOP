from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Famiglia(Base):
    __tablename__ = "famiglie"
    
    id = Column(Integer, primary_key=True, index=True)
    cognome = Column(String, index=True, nullable=False)
    num_adulti = Column(Integer, default=1)
    num_bambini = Column(Integer, default=1)
    num_ragazzi = Column(Integer, default=1)
