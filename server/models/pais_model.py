from pydantic import BaseModel, Field

class Pais(BaseModel):
    id: str = Field(default=None)
    nombre: str = Field(default=None)
    email: str = Field(default=None)
    lat: float = Field(default=None)
    lon: float = Field(default=None)
    imagen: str = Field(default=None)

class PaisCreate(BaseModel):
    nombre: str = Field(default=None, validate_default=True)
    email: str = Field(default=None, validate_default=True)
    lat: float = Field(default=None, validate_default=True)
    lon: float = Field(default=None, validate_default=True)
    imagen: str = Field(default=None, validate_default=True)

class PaisUpdate(BaseModel):
    nombre: str | None = Field(default=None)
    email: str | None = Field(default=None)
    lat: float | None = Field(default=None)
    lon: float | None = Field(default=None)
    imagen: str | None = Field(default=None)

class PaisDeleteResponse(BaseModel):
    details: str = "El país se ha eliminado correctamente."