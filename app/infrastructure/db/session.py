# app/infrastructure/db/session.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.infrastructure.config.settings import Settings


class DatabaseManager:
    """Manages database connection and sessions"""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.engine = None
        self.async_session = None

    async def initialize(self):
        """Initialize database engine and session"""
        self.engine = create_async_engine(
            self.settings.database_url,
            echo=self.settings.sql_echo,
            future=True,
        )
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncSession:
        """Get async session"""
        async with self.async_session() as session:
            yield session

    async def close(self):
        """Close database connection"""
        if self.engine:
            await self.engine.dispose()

    async def create_tables(self):
        """Create all tables"""
        from app.infrastructure.db.models import Base
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self):
        """Drop all tables"""
        from app.infrastructure.db.models import Base
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
