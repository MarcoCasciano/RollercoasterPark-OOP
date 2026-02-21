from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.giro import GiroRead


class VisitatoreBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    cognome: str = Field(..., min_length=1, max_length=100)
    tipo: Literal["bambino", "ragazzo", "adulto"]
    posizione_x: int = 0
    posizione_y: int = 0
    famiglia_id: int | None = None


class VisitatoreCreate(VisitatoreBase):
    pass


class VisitatoreUpdate(BaseModel):
    nome: str | None = None
    cognome: str | None = None
    tipo: Literal["bambino", "ragazzo", "adulto"] | None = None
    posizione_x: int | None = None
    posizione_y: int | None = None
    famiglia_id: int | None = None


class VisitatoreRead(VisitatoreBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    giri: list[GiroRead] = []
