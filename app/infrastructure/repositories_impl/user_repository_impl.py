# app/infrastructure/repositories_impl/user_repository_impl.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.entities.user_entity import User, Email
from app.domain.respositories.user_repositories import UserRepository
from app.infrastructure.db.models import UserModel


class UserRepositoryImpl(UserRepository):
    """Implementation: User persistence using SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> None:
        """Save or update a user"""
        existing = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id.value)
        )
        model = existing.scalars().first()

        if model:
            # Update existing
            model.name = user.name
            model.email = user.email.value
            model.is_active = user.is_active
            model.updated_at = user.updated_at
        else:
            # Create new
            model = UserModel.from_domain(user)
            self.session.add(model)

        await self.session.commit()

    async def get_by_id(self, user_id: str) -> User | None:
        """Get user by ID"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalars().first()
        return model.to_domain() if model else None

    async def get_by_email(self, email: Email) -> User | None:
        """Get user by email"""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email.value)
        )
        model = result.scalars().first()
        return model.to_domain() if model else None

    async def delete(self, user_id: str) -> None:
        """Delete a user"""
        await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalars().first()
        if model:
            await self.session.delete(model)
            await self.session.commit()

    async def list_all(self) -> list[User]:
        """List all users"""
        result = await self.session.execute(select(UserModel))
        models = result.scalars().all()
        return [model.to_domain() for model in models]
