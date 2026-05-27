# app/domain/repositories/user_repository.py

from typing import Protocol
from app.domain.entities.user_entity import User, Email


class UserRepository(Protocol):
    """Repository Interface: User persistence abstraction"""

    async def save(self, user: User) -> None:
        """Save or update a user"""
        ...

    async def get_by_id(self, user_id: str) -> User | None:
        """Get user by ID"""
        ...

    async def get_by_email(self, email: Email) -> User | None:
        """Get user by email"""
        ...

    async def delete(self, user_id: str) -> None:
        """Delete a user"""
        ...

    async def list_all(self) -> list[User]:
        """List all users"""
        ...