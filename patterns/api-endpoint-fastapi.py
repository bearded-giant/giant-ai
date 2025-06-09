"""
Example target pattern for consistent FastAPI endpoints
Use with: ai-pattern-refactor refactor "FastAPI routes" --target-pattern patterns/api-endpoint-fastapi.py
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from app.models import User
from app.schemas import (
    CreateUserRequest, 
    UserResponse, 
    PaginatedResponse,
    ErrorResponse
)
from app.services import UserService
from app.dependencies import get_current_user, get_user_service
from app.exceptions import AppError

logger = logging.getLogger(__name__)

# Router with prefix and tags
router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    responses={
        404: {"model": ErrorResponse, "description": "Not found"},
        422: {"model": ErrorResponse, "description": "Validation error"}
    }
)


# Dependency for consistent error responses
async def handle_app_errors(func):
    """Decorator for consistent error handling"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AppError as e:
            logger.warning(f"Application error: {e.code} - {e.message}")
            raise HTTPException(
                status_code=e.status_code,
                detail={
                    "code": e.code,
                    "message": e.message,
                    "details": e.details
                }
            )
        except Exception as e:
            logger.exception("Unexpected error in API endpoint")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred"
                }
            )
    return wrapper


# Consistent endpoint pattern with proper typing
@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided data",
    response_model_exclude_unset=True
)
async def create_user(
    user_data: CreateUserRequest,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """Create a new user endpoint with full validation and error handling"""
    
    # Log the request with context
    logger.info(
        "Creating new user",
        extra={
            "email": user_data.email,
            "requested_by": current_user.id,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
    
    try:
        # Business logic in service layer
        user = await user_service.create_user(user_data.dict())
        
        # Return typed response
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            metadata={
                "created_by": current_user.id,
                "version": "v1"
            }
        )
        
    except ValueError as e:
        # Convert domain errors to HTTP errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "VALIDATION_ERROR",
                "message": str(e)
            }
        )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    responses={
        200: {"description": "User found", "model": UserResponse},
        404: {"description": "User not found", "model": ErrorResponse}
    }
)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """Get a specific user by ID"""
    
    logger.debug(f"Fetching user {user_id} for {current_user.id}")
    
    user = await user_service.get_user(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "USER_NOT_FOUND",
                "message": f"User {user_id} not found"
            }
        )
    
    return UserResponse.from_orm(user)


@router.get(
    "",
    response_model=PaginatedResponse[UserResponse],
    summary="List users",
    description="Get paginated list of users with optional filtering"
)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    search: Optional[str] = Query(None, description="Search term"),
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
) -> PaginatedResponse[UserResponse]:
    """List users with pagination and filtering"""
    
    logger.info(
        f"Listing users",
        extra={
            "page": page,
            "per_page": per_page,
            "requested_by": current_user.id
        }
    )
    
    # Get paginated results from service
    result = await user_service.list_users(
        page=page,
        per_page=per_page,
        sort_by=sort_by,
        sort_order=sort_order,
        search=search
    )
    
    # Convert to response model
    return PaginatedResponse(
        items=[UserResponse.from_orm(user) for user in result.items],
        total=result.total,
        page=page,
        per_page=per_page,
        pages=result.pages,
        metadata={
            "sort_by": sort_by,
            "sort_order": sort_order,
            "search": search
        }
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user"
)
async def update_user(
    user_id: int,
    user_data: UpdateUserRequest,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """Update user information"""
    
    # Check permissions
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "PERMISSION_DENIED",
                "message": "You can only update your own profile"
            }
        )
    
    updated_user = await user_service.update_user(
        user_id, 
        user_data.dict(exclude_unset=True)
    )
    
    return UserResponse.from_orm(updated_user)


# Exception handler for consistent error responses
@router.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError):
    """Handle value errors consistently"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "error": {
                "code": "INVALID_VALUE",
                "message": str(exc)
            }
        }
    )