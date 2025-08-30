"""
Example target pattern for consistent pytest test structure
Use with: ai-pattern-refactor refactor "test functions" --target-pattern patterns/test-pattern-pytest.py
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
from typing import Dict, Any

from app.services import UserService
from app.models import User
from app.exceptions import AppError, ValidationError


class TestUserService:
    """Test class for UserService with consistent patterns"""

    @pytest.fixture
    def user_service(self):
        """Fixture for UserService instance"""
        return UserService()

    @pytest.fixture
    def mock_user_data(self) -> Dict[str, Any]:
        """Fixture for test user data"""
        return {
            "email": "test@example.com",
            "name": "Test User",
            "password": "securepassword123",
        }

    @pytest.fixture
    def mock_user(self, mock_user_data) -> User:
        """Fixture for mock User instance"""
        return User(
            id=1,
            **mock_user_data,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

    # Test naming: test_<method>_<scenario>_<expected_result>

    def test_create_user_valid_data_returns_user(
        self, user_service, mock_user_data, mock_user
    ):
        """Test successful user creation with valid data"""
        # Arrange
        with patch.object(user_service, "_hash_password") as mock_hash:
            mock_hash.return_value = "hashed_password"
            with patch.object(user_service.repository, "create") as mock_create:
                mock_create.return_value = mock_user

                # Act
                result = user_service.create_user(mock_user_data)

                # Assert
                assert result.id == mock_user.id
                assert result.email == mock_user_data["email"]
                mock_hash.assert_called_once_with(mock_user_data["password"])
                mock_create.assert_called_once()

    def test_create_user_duplicate_email_raises_error(
        self, user_service, mock_user_data
    ):
        """Test user creation with duplicate email raises appropriate error"""
        # Arrange
        with patch.object(user_service.repository, "get_by_email") as mock_get:
            mock_get.return_value = Mock()  # User already exists

            # Act & Assert
            with pytest.raises(ValidationError) as exc_info:
                user_service.create_user(mock_user_data)

            assert "already exists" in str(exc_info.value)
            assert exc_info.value.code == "DUPLICATE_EMAIL"

    def test_get_user_existing_id_returns_user(self, user_service, mock_user):
        """Test getting existing user by ID"""
        # Arrange
        user_id = 1
        with patch.object(user_service.repository, "get_by_id") as mock_get:
            mock_get.return_value = mock_user

            # Act
            result = user_service.get_user(user_id)

            # Assert
            assert result == mock_user
            mock_get.assert_called_once_with(user_id)

    def test_get_user_nonexistent_id_returns_none(self, user_service):
        """Test getting non-existent user returns None"""
        # Arrange
        user_id = 999
        with patch.object(user_service.repository, "get_by_id") as mock_get:
            mock_get.return_value = None

            # Act
            result = user_service.get_user(user_id)

            # Assert
            assert result is None
            mock_get.assert_called_once_with(user_id)

    @pytest.mark.parametrize(
        "invalid_email", ["", "not-an-email", "@example.com", "user@", None]
    )
    def test_create_user_invalid_email_raises_validation_error(
        self, user_service, mock_user_data, invalid_email
    ):
        """Test user creation with various invalid emails"""
        # Arrange
        mock_user_data["email"] = invalid_email

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            user_service.create_user(mock_user_data)

        assert "Invalid email" in str(exc_info.value)


# Async test patterns
class TestAsyncUserService:
    """Test patterns for async service methods"""

    @pytest.fixture
    def async_user_service(self):
        """Fixture for async UserService"""
        return AsyncUserService()

    @pytest.mark.asyncio
    async def test_fetch_user_data_success(self, async_user_service):
        """Test async user data fetching"""
        # Arrange
        user_id = 1
        expected_data = {"id": user_id, "name": "Test User"}

        with patch.object(async_user_service, "fetch_from_api") as mock_fetch:
            mock_fetch.return_value = expected_data

            # Act
            result = await async_user_service.fetch_user_data(user_id)

            # Assert
            assert result == expected_data
            mock_fetch.assert_called_once_with(f"/users/{user_id}")

    @pytest.mark.asyncio
    async def test_batch_process_users_handles_failures(self, async_user_service):
        """Test batch processing with partial failures"""
        # Arrange
        user_ids = [1, 2, 3]

        async def mock_process(user_id):
            if user_id == 2:
                raise ValueError("Processing failed")
            return {"id": user_id, "processed": True}

        with patch.object(async_user_service, "process_user", side_effect=mock_process):
            # Act
            results = await async_user_service.batch_process_users(user_ids)

            # Assert
            assert len(results) == 3
            assert results[0]["processed"] is True
            assert results[1] is None  # Failed item
            assert results[2]["processed"] is True


# Integration test pattern
@pytest.mark.integration
class TestUserServiceIntegration:
    """Integration tests with real database"""

    @pytest.fixture
    def db_session(self):
        """Fixture for database session"""
        # Setup test database
        session = create_test_session()
        yield session
        # Cleanup
        session.rollback()
        session.close()

    def test_create_and_retrieve_user_integration(self, db_session):
        """Test full user creation and retrieval flow"""
        # Arrange
        service = UserService(db_session)
        user_data = {
            "email": f"test_{datetime.utcnow().timestamp()}@example.com",
            "name": "Integration Test User",
            "password": "testpass123",
        }

        # Act - Create user
        created_user = service.create_user(user_data)

        # Act - Retrieve user
        retrieved_user = service.get_user(created_user.id)

        # Assert
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.email == user_data["email"]
        assert retrieved_user.name == user_data["name"]
