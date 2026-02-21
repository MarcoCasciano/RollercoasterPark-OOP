from pydantic import BaseModel, ConfigDict, Field


# -------------------------
# Base schema (campi comuni)
# -------------------------
class AttrazioneBase(BaseModel):
    nome: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nome univoco dell'attrazione"
    )
    per_bambini: bool = True
    capienza_massima: int = Field(
        default=5,
        ge=1,
        description="Numero massimo di visitatori per giro"
    )
    durata_giro: int = Field(
        default=2,
        ge=1,
        description="Durata del giro in minuti"
    )
    posizione_x: float = 0.0
    posizione_y: float = 0.0


# -------------------------
# Schema per CREATE (POST)
# -------------------------
class AttrazioneCreate(AttrazioneBase):
    pass


# -------------------------
# Schema per UPDATE (PATCH)
# -------------------------
class AttrazioneUpdate(BaseModel):
    nome: str | None = None
    per_bambini: bool | None = None
    capienza_massima: int | None = Field(default=None, ge=1)
    durata_giro: int | None = Field(default=None, ge=1)
    posizione_x: float | None = None
    posizione_y: float | None = None


# -------------------------
# Schema per READ (RESPONSE)
# -------------------------
class AttrazioneRead(AttrazioneBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
