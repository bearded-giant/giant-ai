"""
Example target pattern for Python dataclasses and type hints
Use with: ai-pattern-refactor refactor "class definitions" --target-pattern patterns/dataclass-pattern.py
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, ClassVar
from datetime import datetime
from enum import Enum
import uuid


class UserRole(Enum):
    """Enumeration for user roles"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


@dataclass(frozen=True)
class Address:
    """Immutable address dataclass"""
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"
    
    def __post_init__(self):
        """Validate address data after initialization"""
        if not self.zip_code.replace("-", "").isdigit():
            raise ValueError(f"Invalid zip code: {self.zip_code}")


@dataclass
class User:
    """User dataclass with proper typing and defaults"""
    # Required fields
    email: str
    name: str
    
    # Optional fields with defaults
    id: Optional[int] = None
    role: UserRole = UserRole.USER
    is_active: bool = True
    address: Optional[Address] = None
    
    # Mutable default using field()
    permissions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Auto-generated fields
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Class variables (not instance fields)
    _valid_roles: ClassVar[List[str]] = ["admin", "user", "guest"]
    
    def __post_init__(self):
        """Validate and normalize data after initialization"""
        # Email validation
        if "@" not in self.email:
            raise ValueError(f"Invalid email: {self.email}")
        
        # Normalize email
        self.email = self.email.lower().strip()
        
        # Name validation
        if not self.name or len(self.name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
    
    def update_timestamp(self) -> None:
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
    
    def add_permission(self, permission: str) -> None:
        """Add a permission if not already present"""
        if permission not in self.permissions:
            self.permissions.append(permission)
            self.update_timestamp()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role.value,
            "is_active": self.is_active,
            "address": self.address.__dict__ if self.address else None,
            "permissions": self.permissions,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "uuid": self.uuid
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Create User instance from dictionary"""
        # Handle address separately
        address_data = data.pop("address", None)
        if address_data:
            address = Address(**address_data)
        else:
            address = None
        
        # Handle role enum
        role_str = data.pop("role", "user")
        role = UserRole(role_str)
        
        # Handle datetime fields
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        
        return cls(
            address=address,
            role=role,
            **data
        )


@dataclass
class APIResponse:
    """Generic API response dataclass"""
    success: bool
    data: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Ensure response is valid"""
        if self.success and self.error:
            raise ValueError("Successful response should not have error")
        if not self.success and not self.error:
            raise ValueError("Failed response must have error details")


# Configuration dataclass with environment defaults
@dataclass
class AppConfig:
    """Application configuration with type hints"""
    app_name: str
    debug: bool = False
    database_url: str = "sqlite:///app.db"
    redis_url: Optional[str] = None
    api_key: Optional[str] = field(default=None, repr=False)  # Hide from repr
    max_connections: int = 100
    timeout_seconds: float = 30.0
    allowed_origins: List[str] = field(default_factory=lambda: ["http://localhost:3000"])
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        """Create config from environment variables"""
        import os
        return cls(
            app_name=os.getenv("APP_NAME", "MyApp"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            database_url=os.getenv("DATABASE_URL", cls.database_url),
            redis_url=os.getenv("REDIS_URL"),
            api_key=os.getenv("API_KEY"),
            max_connections=int(os.getenv("MAX_CONNECTIONS", str(cls.max_connections))),
            timeout_seconds=float(os.getenv("TIMEOUT_SECONDS", str(cls.timeout_seconds)))
        )