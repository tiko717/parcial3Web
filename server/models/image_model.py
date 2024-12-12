from pydantic import BaseModel, Field
from datetime import datetime

class Image(BaseModel):
    """
    Modelo de datos para representar imágenes. Los atributos no pueden ser modificados ni eliminados
    una vez creados.

    Attributes
    ----------
    name : str
        Nombre de la imagen (obligatorio)
    ownerId : int
        ID del propietario de la imagen (obligatorio)
    url : str
        URL de acceso a la imagen (obligatorio)
    date : str
        Fecha de creación de la imagen en formato ISO (obligatorio)
    """
    name: str = Field(default=None, example="profile_picture.png")
    ownerId: int = Field(default=None, example=1)
    url: str = Field(default=None, example="https://res.cloudinary.com/demo/image/upload/v1234567890/sample.jpg")
    timestamp: str = Field(default=datetime.now().isoformat(), example=datetime.now().isoformat())
