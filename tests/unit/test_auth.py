"""Unit tests for authentication routes."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.user import User
from app.core.security import hash_password

client = TestClient(app)


@pytest.fixture
def test_user(db: Session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        full_name="Test User",
        hashed_password=hash_password("testpass123"),
        role="USER",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_register_success():
    """Test successful user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "SecurePass123",
            "full_name": "New User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert data["role"] == "USER"


def test_register_duplicate_email(test_user):
    """Test registration with duplicate email."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "SecurePass123",
            "full_name": "Another User",
        },
    )
    assert response.status_code == 409


def test_login_success(test_user):
    """Test successful login."""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "testpass123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401
