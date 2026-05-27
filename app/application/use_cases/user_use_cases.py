# app/application/use_cases/user_use_cases.py

from app.domain.entities.user_entity import User
from app.domain.services.user_domain_service import UserDomainService
from app.domain.exceptions.user_exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidEmailError,
    InvalidUserNameError
)
from app.application.dto.user_dto import UserResponse


class CreateUserUseCase:
    """Use Case: Create a new user"""

    def __init__(self, user_domain_service: UserDomainService):
        self.user_domain_service = user_domain_service

    async def execute(self, email: str, name: str) -> UserResponse:
        """Execute create user use case"""
        try:
            if not name or len(name.strip()) == 0:
                raise InvalidUserNameError(name)

            user = await self.user_domain_service.create_user(email, name)
            return self._user_to_response(user)
        except UserAlreadyExistsError as e:
            raise e
        except ValueError as e:
            raise InvalidEmailError(email)

    @staticmethod
    def _user_to_response(user: User) -> UserResponse:
        return UserResponse(
            id=user.id.value,
            email=user.email.value,
            name=user.name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class GetUserByIdUseCase:
    """Use Case: Get user by ID"""

    def __init__(self, user_domain_service: UserDomainService):
        self.user_domain_service = user_domain_service

    async def execute(self, user_id: str) -> UserResponse:
        """Execute get user use case"""
        user = await self.user_domain_service.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return self._user_to_response(user)

    @staticmethod
    def _user_to_response(user: User) -> UserResponse:
        return UserResponse(
            id=user.id.value,
            email=user.email.value,
            name=user.name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class UpdateUserNameUseCase:
    """Use Case: Update user name"""

    def __init__(self, user_domain_service: UserDomainService):
        self.user_domain_service = user_domain_service

    async def execute(self, user_id: str, name: str) -> UserResponse:
        """Execute update user name use case"""
        if not name or len(name.strip()) == 0:
            raise InvalidUserNameError(name)

        user = await self.user_domain_service.update_user_name(user_id, name)
        return self._user_to_response(user)

    @staticmethod
    def _user_to_response(user: User) -> UserResponse:
        return UserResponse(
            id=user.id.value,
            email=user.email.value,
            name=user.name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class DeactivateUserUseCase:
    """Use Case: Deactivate user"""

    def __init__(self, user_domain_service: UserDomainService):
        self.user_domain_service = user_domain_service

    async def execute(self, user_id: str) -> UserResponse:
        """Execute deactivate user use case"""
        user = await self.user_domain_service.deactivate_user(user_id)
        return self._user_to_response(user)

    @staticmethod
    def _user_to_response(user: User) -> UserResponse:
        return UserResponse(
            id=user.id.value,
            email=user.email.value,
            name=user.name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class ListAllUsersUseCase:
    """Use Case: List all users"""

    def __init__(self, user_domain_service: UserDomainService):
        self.user_domain_service = user_domain_service

    async def execute(self) -> list[UserResponse]:
        """Execute list all users use case"""
        users = await self.user_domain_service.user_repository.list_all()
        return [self._user_to_response(user) for user in users]

    @staticmethod
    def _user_to_response(user: User) -> UserResponse:
        return UserResponse(
            id=user.id.value,
            email=user.email.value,
            name=user.name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
