# app/domain/exceptions/user_exceptions.py


class UserDomainException(Exception):
    """Base exception for user domain"""
    pass


class UserNotFoundError(UserDomainException):
    """User not found"""
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User with ID {user_id} not found")


class UserAlreadyExistsError(UserDomainException):
    """User already exists with email"""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email {email} already exists")


class InvalidEmailError(UserDomainException):
    """Invalid email format"""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Invalid email format: {email}")


class InvalidUserNameError(UserDomainException):
    """Invalid user name"""
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Invalid user name: {name}")
