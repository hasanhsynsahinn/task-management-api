"""Integration tests for authentication flow."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_full_auth_flow():
    """Test complete authentication flow."""
    # Register
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "integration@example.com",
            "password": "IntegrationPass123",
            "full_name": "Integration Test",
        },
    )
    assert register_response.status_code == 201

    # Login
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "integration@example.com",
            "password": "IntegrationPass123",
        },
    )
    assert login_response.status_code == 200
    data = login_response.json()
    access_token = data["access_token"]

    # Get current user
    user_response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert user_response.status_code == 200
    user_data = user_response.json()
    assert user_data["email"] == "integration@example.com"
