# app/infrastructure/db/models.py

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class UserModel(Base):
    """SQLAlchemy model for User entity"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_domain(self):
        """Convert ORM model to domain entity"""
        from app.domain.entities.user_entity import User, UserId, Email
        return User(
            id=UserId(self.id),
            email=Email(self.email),
            name=self.name,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_domain(user):
        """Convert domain entity to ORM model"""
        return UserModel(
            id=user.id.value,
            email=user.email.value,
            name=user.name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
