# app/application/dto/user_dto.py

from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel, EmailStr


# Request DTOs
class CreateUserRequest(BaseModel):
    """DTO for creating a user"""
    email: EmailStr
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe"
            }
        }


class UpdateUserRequest(BaseModel):
    """DTO for updating a user"""
    name: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Doe"
            }
        }


# Response DTOs
@dataclass
class UserResponse:
    """DTO for user response"""
    id: str
    email: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class UserResponseModel(BaseModel):
    """Pydantic model for user response"""
    id: str
    email: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
