"""
Example target pattern for consistent Flask API endpoints
Use with: ai-pattern-refactor refactor "Flask routes" --target-pattern patterns/api-endpoint-flask.py
"""

from flask import Blueprint, request, jsonify
from functools import wraps
from typing import Dict, Any, Tuple, Callable
from datetime import datetime
import logging

from app.models import User
from app.schemas import CreateUserSchema, UserResponseSchema
from app.services import UserService
from app.exceptions import AppError, ValidationError
from app.auth import require_auth

logger = logging.getLogger(__name__)

# Blueprint for users API
users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')


def validate_request(schema_class):
    """Decorator for request validation"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Validate request data
                schema = schema_class()
                data = schema.load(request.get_json() or {})
                request.validated_data = data
            except ValidationError as e:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Invalid request data',
                        'details': e.messages
                    }
                }), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def handle_errors(f):
    """Decorator for consistent error handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AppError as e:
            # Handle known application errors
            logger.warning(f"Application error: {e.code} - {e.message}")
            return jsonify({
                'success': False,
                'error': {
                    'code': e.code,
                    'message': e.message,
                    'details': e.details
                }
            }), e.status_code
        except Exception as e:
            # Handle unexpected errors
            logger.exception("Unexpected error in API endpoint")
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': 'An unexpected error occurred'
                }
            }), 500
    return decorated_function


def create_response(data: Any, status_code: int = 200, metadata: Dict[str, Any] = None) -> Tuple[Dict, int]:
    """Create consistent API response"""
    response = {
        'success': True,
        'data': data,
        'metadata': {
            'timestamp': datetime.utcnow().isoformat(),
            'version': 'v1',
            **(metadata or {})
        }
    }
    return jsonify(response), status_code


# Consistent endpoint pattern
@users_bp.route('', methods=['POST'])
@require_auth()
@validate_request(CreateUserSchema)
@handle_errors
def create_user():
    """Create a new user"""
    # Log the request
    logger.info(
        "Creating new user",
        extra={
            'email': request.validated_data.get('email'),
            'ip_address': request.remote_addr
        }
    )
    
    # Business logic in service layer
    user_service = UserService()
    user = user_service.create_user(request.validated_data)
    
    # Serialize response
    response_schema = UserResponseSchema()
    user_data = response_schema.dump(user)
    
    # Return consistent response
    return create_response(
        data=user_data,
        status_code=201,
        metadata={'user_id': user.id}
    )


@users_bp.route('/<int:user_id>', methods=['GET'])
@require_auth()
@handle_errors
def get_user(user_id: int):
    """Get user by ID"""
    logger.debug(f"Fetching user {user_id}")
    
    user_service = UserService()
    user = user_service.get_user(user_id)
    
    if not user:
        raise AppError(
            message=f"User {user_id} not found",
            code="USER_NOT_FOUND",
            status_code=404
        )
    
    response_schema = UserResponseSchema()
    user_data = response_schema.dump(user)
    
    return create_response(data=user_data)


@users_bp.route('', methods=['GET'])
@require_auth()
@handle_errors
def list_users():
    """List users with pagination"""
    # Parse query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    sort_by = request.args.get('sort_by', 'created_at')
    
    # Validate pagination parameters
    per_page = min(per_page, 100)  # Max 100 items per page
    
    logger.info(f"Listing users: page={page}, per_page={per_page}")
    
    user_service = UserService()
    paginated_result = user_service.list_users(
        page=page,
        per_page=per_page,
        sort_by=sort_by
    )
    
    response_schema = UserResponseSchema(many=True)
    users_data = response_schema.dump(paginated_result.items)
    
    return create_response(
        data=users_data,
        metadata={
            'page': page,
            'per_page': per_page,
            'total': paginated_result.total,
            'pages': paginated_result.pages
        }
    )


# Error handler for the blueprint
@users_bp.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'success': False,
        'error': {
            'code': 'NOT_FOUND',
            'message': 'Resource not found'
        }
    }), 404