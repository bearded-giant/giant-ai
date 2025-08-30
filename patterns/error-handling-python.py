"""
Example target pattern for consistent Python error handling
Use with: ai-pattern-refactor refactor "exception handling" --target-pattern patterns/error-handling-python.py
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime

# Configure structured logging
logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base application error with consistent structure"""

    def __init__(
        self,
        message: str,
        code: str = "APP_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        self.timestamp = datetime.utcnow().isoformat()


def example_operation(data: Dict[str, Any]) -> Dict[str, Any]:
    """Example of consistent error handling pattern"""
    operation_id = data.get("id", "unknown")

    try:
        # Input validation
        if not data:
            raise AppError(
                "Invalid input data",
                code="VALIDATION_ERROR",
                status_code=400,
                details={"received": data},
            )

        # Main operation logic
        result = perform_operation(data)

        # Success logging with context
        logger.info(
            "Operation completed successfully",
            extra={
                "operation_id": operation_id,
                "result_id": result.get("id"),
                "duration_ms": result.get("duration_ms"),
            },
        )

        return {
            "success": True,
            "data": result,
            "metadata": {
                "operation_id": operation_id,
                "timestamp": datetime.utcnow().isoformat(),
            },
        }

    except AppError:
        # Re-raise application errors (they're already properly formatted)
        raise

    except ValidationError as e:
        # Convert known exceptions to AppError
        logger.warning(
            "Validation failed",
            extra={"operation_id": operation_id, "validation_errors": e.errors},
        )
        raise AppError(
            f"Validation failed: {str(e)}",
            code="VALIDATION_ERROR",
            status_code=400,
            details={"errors": e.errors},
        )

    except Exception as e:
        # Log unexpected errors with full context
        logger.exception(
            "Unexpected error in operation",
            extra={
                "operation_id": operation_id,
                "error_type": type(e).__name__,
                "error_message": str(e),
            },
        )

        # Convert to AppError for consistent API responses
        raise AppError(
            "An unexpected error occurred",
            code="INTERNAL_ERROR",
            status_code=500,
            details={"operation_id": operation_id, "error_type": type(e).__name__},
        ) from e


# Context manager for error handling
from contextlib import contextmanager


@contextmanager
def error_handler(operation_name: str, **context):
    """Context manager for consistent error handling"""
    try:
        logger.debug(f"Starting {operation_name}", extra=context)
        yield
        logger.debug(f"Completed {operation_name}", extra=context)
    except Exception as e:
        logger.exception(
            f"Error in {operation_name}",
            extra={**context, "error_type": type(e).__name__, "error_message": str(e)},
        )
        raise


# Usage example
def process_user_data(user_id: int) -> Dict[str, Any]:
    """Example using the error handling context manager"""
    with error_handler("process_user_data", user_id=user_id):
        user = fetch_user(user_id)
        result = transform_user_data(user)
        save_processed_data(result)
        return result
