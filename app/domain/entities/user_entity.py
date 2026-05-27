from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class UserId:
    """Value Object: User ID"""
    value: str = field(default_factory=lambda: str(uuid4()))

    def __eq__(self, other):
        if not isinstance(other, UserId):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


@dataclass
class Email:
    """Value Object: Email"""
    value: str

    def __post_init__(self):
        if "@" not in self.value:
            raise ValueError("Invalid email format")
        self.value = self.value.lower()

    def __eq__(self, other):
        if not isinstance(other, Email):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)


@dataclass
class User:
    """Entity: User - The main aggregate root"""
    id: UserId
    email: Email
    name: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def update_name(self, name: str) -> None:
        """Domain logic: Update user name"""
        if not name or len(name.strip()) == 0:
            raise ValueError("Name cannot be empty")
        self.name = name
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Domain logic: Deactivate user"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Domain logic: Activate user"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    @staticmethod
    def create(email: str, name: str) -> "User":
        """Factory method: Create new user"""
        return User(
            id=UserId(),
            email=Email(email),
            name=name,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )