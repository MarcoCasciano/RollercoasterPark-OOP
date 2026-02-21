from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GiroBase(BaseModel):
    visitatore_id: int
    attrazione_id: int
    ciclo: int = 0


class GiroCreate(GiroBase):
    pass


class GiroRead(GiroBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
