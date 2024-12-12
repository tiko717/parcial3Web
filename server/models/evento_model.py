from pydantic import BaseModel, Field

from pydantic import BaseModel, Field
from datetime import datetime

class Evento(BaseModel):
    id: str = Field(default=None)
    nombre: str = Field(default=None)
    timestamp: str = Field(default=None)
    lugar: str = Field(default=None)
    lat: float = Field(default=None)
    lon: float = Field(default=None)
    organizador: str = Field(default=None)
    imagen: str = Field(default=None)

class EventoCreate(BaseModel):
    nombre: str = Field(default=None, validate_default=True)
    timestamp: str = Field(default=None, validate_default=True)
    lugar: str = Field(default=None, validate_default=True)
    lat: float = Field(default=None, validate_default=True)
    lon: float = Field(default=None, validate_default=True)
    organizador: str = Field(default=None, validate_default=True)
    imagen: str = Field(default=None, validate_default=True)

class EventoUpdate(BaseModel):
    nombre: str | None = Field(default=None)
    timestamp: str | None = Field(default=None)
    lugar: str | None = Field(default=None)
    lat: float | None = Field(default=None)
    lon: float | None = Field(default=None)
    organizador: str | None = Field(default=None)
    imagen: str | None = Field(default=None)

class EventoDeleteResponse(BaseModel):
    details: str = "El evento se ha eliminado correctamente."