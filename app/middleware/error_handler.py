# app/middleware/error_handler.py

from fastapi import Request
from starlette.responses import JSONResponse
from app.domain.exceptions.user_exceptions import UserDomainException


async def user_exception_handler(request: Request, exc: UserDomainException):
    """Handle user domain exceptions"""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )
