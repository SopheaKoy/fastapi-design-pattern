# app/presentation/api/v1/user_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.user_dto import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponseModel,
)
from app.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    GetUserByIdUseCase,
    UpdateUserNameUseCase,
    DeactivateUserUseCase,
    ListAllUsersUseCase,
)
from app.domain.services.user_domain_service import UserDomainService
from app.infrastructure.repositories_impl.user_repository_impl import UserRepositoryImpl
from app.domain.exceptions.user_exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    InvalidEmailError,
    InvalidUserNameError,
)

router = APIRouter(prefix="/api/v1/users", tags=["users"])


# Dependency injection - this will be set by the app
def get_session_dependency() -> AsyncSession:
    """Placeholder for session dependency - will be set by the app"""
    raise NotImplementedError("This dependency should be overridden by the app")


async def get_user_repository(
    session: AsyncSession = Depends(get_session_dependency),
) -> UserRepositoryImpl:
    """Get user repository"""
    return UserRepositoryImpl(session)


def get_user_domain_service(
    repository: UserRepositoryImpl = Depends(get_user_repository),
) -> UserDomainService:
    """Get user domain service"""
    return UserDomainService(repository)


# Routes
@router.post("/", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    domain_service: UserDomainService = Depends(get_user_domain_service),
):
    """Create a new user"""
    try:
        use_case = CreateUserUseCase(domain_service)
        response = await use_case.execute(request.email, request.name)
        return UserResponseModel(**response.to_dict())
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except (InvalidEmailError, InvalidUserNameError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{user_id}", response_model=UserResponseModel)
async def get_user(
    user_id: str,
    domain_service: UserDomainService = Depends(get_user_domain_service),
):
    """Get user by ID"""
    try:
        use_case = GetUserByIdUseCase(domain_service)
        response = await use_case.execute(user_id)
        return UserResponseModel(**response.to_dict())
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )


@router.put("/{user_id}", response_model=UserResponseModel)
async def update_user(
    user_id: str,
    request: UpdateUserRequest,
    domain_service: UserDomainService = Depends(get_user_domain_service),
):
    """Update user"""
    try:
        if request.name:
            use_case = UpdateUserNameUseCase(domain_service)
            response = await use_case.execute(user_id, request.name)
            return UserResponseModel(**response.to_dict())
    except InvalidUserNameError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{user_id}")
async def deactivate_user(
    user_id: str,
    domain_service: UserDomainService = Depends(get_user_domain_service),
):
    """Deactivate user"""
    try:
        use_case = DeactivateUserUseCase(domain_service)
        response = await use_case.execute(user_id)
        return {"message": "User deactivated", "user": UserResponseModel(**response.to_dict())}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/", response_model=list[UserResponseModel])
async def list_users(
    domain_service: UserDomainService = Depends(get_user_domain_service),
):
    """List all users"""
    use_case = ListAllUsersUseCase(domain_service)
    responses = await use_case.execute()
    return [UserResponseModel(**resp.to_dict()) for resp in responses]
