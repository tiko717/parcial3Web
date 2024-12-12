from pydantic import BaseModel, Field
from typing import List

class Review(BaseModel):
    user: str = Field(default=None, example="5f3c3e7d7f43b5a3b1c1e123")
    rating: int = Field(default=None, example=5, ge=0, le=5)

class User(BaseModel):
    id: str = Field(default=None, example="5f3c3e7d7f43b5a3b1c1e123")
    email: str = Field(default=None, example="john.doe@example.com")
    name: str = Field(default=None, example="John")
    surname: str = Field(default=None, example="Doe")  # <- Corregido aquí
    description: str = Field(default=None, example="John Doe is a software engineer.")
    userName: str = Field(default=None, example="johndoe")
    oauthId: str = Field(default="abcd1234", example="abcd1234")
    oauthProvider: str = Field(default="google", example="google")
    oauthToken: str = Field(default=None, example="abcd1234")
    profilePicture: str = Field(default="https://example.com/profile.jpg", example="https://example.com/profile.jpg")
    reviews: List[Review] = Field(default_factory=list, example=[{
        "user": "5f3c3e7d7f43b5a3b1c1e123",
        "rating": 5
    }])

class UserCreate(BaseModel):
    email: str = Field(default=None, example="5f3c3e7d7f43b5a3b1c1e123", validate_default=True)
    name: str = Field(default=None, example="John Doe", validate_default=True)
    surname: str = Field(default=None, example="Doe", validate_default=True)
    description: str = Field(default=None, example="John Doe is a software engineer.", validate_default=True)
    userName: str = Field(default=None, example="johndoe", validate_default=True)
    oauthId: str = Field(default=None, example="abcd1234", validate_default=True)
    oauthProvider: str = Field(default=None, example="google", validate_default=True)
    oauthToken: str = Field(default=None, example="abcd1234", validate_default=True)
    profilePicture: str = Field(default=None, example="https://example.com/profile.jpg", validate_default=True)

class UserUpdate(BaseModel):
    email: str = Field(default=None, example="5f3c3e7d7f43b5a3b1c1e123", validate_default=True)
    name: str = Field(default=None, example="John Doe", validate_default=True)
    surname: str = Field(default=None, example="Doe", validate_default=True)
    description: str = Field(default=None, example="John Doe is a software engineer.", validate_default=True)
    profilePicture: str = Field(default=None, example="https://example.com/profile.jpg", validate_default=True)

    reviews: List[Review] = Field(default_factory=list, example=[{
        "user": "5f3c3e7d7f43b5a3b1c1e123",
        "rating": 5
    }])

class UserDeleteResponse(BaseModel):
    details: str = "El usuario se ha borrado correctamente."
