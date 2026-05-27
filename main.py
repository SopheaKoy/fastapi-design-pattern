from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.config.settings import settings
from app.infrastructure.db.session import DatabaseManager
from app.presentation.api.v1.user_routes import router as user_router
from app.middleware.error_handler import user_exception_handler
from app.domain.exceptions.user_exceptions import UserDomainException

# Database manager
db_manager = DatabaseManager(settings)


# Dependency to get database session
async def get_db_session() -> AsyncSession: # type: ignore
    """Dependency for getting database session"""
    async for session in db_manager.get_session():
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager"""
    # Startup
    await db_manager.initialize()
    await db_manager.create_tables()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    await db_manager.close()
    print("❌ Database closed")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

# Set dependency overrides for database session
app.dependency_overrides[AsyncSession] = get_db_session

# Register routes
app.include_router(user_router)

# Register exception handlers
app.add_exception_handler(UserDomainException, user_exception_handler)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "app": settings.app_name}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

