# app/domain/services/user_domain_service.py

from app.domain.entities.user_entity import User, Email
from app.domain.respositories.user_repositories import UserRepository
from app.domain.exceptions.user_exceptions import UserAlreadyExistsError


class UserDomainService:
    """Domain Service: User business logic that spans entities"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, email: str, name: str) -> User:
        """Create a new user with domain logic validation"""
        email_vo = Email(email)

        # Check if user already exists
        existing_user = await self.user_repository.get_by_email(email_vo)
        if existing_user:
            raise UserAlreadyExistsError(email)

        # Create user using factory method
        user = User.create(email, name)

        # Save to repository
        await self.user_repository.save(user)

        return user

    async def update_user_name(self, user_id: str, new_name: str) -> User:
        """Update user name with domain logic"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        user.update_name(new_name)
        await self.user_repository.save(user)

        return user

    async def deactivate_user(self, user_id: str) -> User:
        """Deactivate user with domain logic"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        user.deactivate()
        await self.user_repository.save(user)

        return user
