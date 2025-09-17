from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError

class SprintSyncException(Exception):
    """Base class for all SprintSync errors"""
    pass

class UserAlreadyExists(SprintSyncException):
    """User has provided an email for a user who exists during sign up"""
    pass

class InvalidCredentials(SprintSyncException):
    """User has provided wrong username or password during log in"""
    pass

class InsufficientPermission(SprintSyncException):
    """User does not have the necessary permissions to perform an action"""
    pass

class UserNotFound(SprintSyncException):
    """User Not found"""
    pass

class TaskNotFound(SprintSyncException):
    """Task Not found"""
    pass

class InvalidToken(SprintSyncException):
    """User has provided an invalid or expired token"""
    pass

def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: SprintSyncException):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler

def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_409_CONFLICT,
            initial_detail={
                "message": "User with username or email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )
    
    app.add_exception_handler(
        TaskNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Task not found",
                "error_code": "task_not_found",
            },
        ),
    )
    
    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Invalid username or password",
                "error_code": "invalid_credentials",
            },
        ),
    )
    
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or expired",
                "resolution": "Please get a new token",
                "error_code": "invalid_token",
            },
        ),
    )
    
    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request, exc):
        return JSONResponse(
            content={
                "message": "Database error occurred",
                "error_code": "database_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )