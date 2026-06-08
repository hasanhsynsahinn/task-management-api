"""Unit tests for task routes."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.core.security import hash_password, create_access_token

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


@pytest.fixture
def test_project(db: Session, test_user: User):
    """Create a test project."""
    project = Project(
        name="Test Project",
        description="A test project",
        owner_id=test_user.id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@pytest.fixture
def auth_headers(test_user: User):
    """Create authentication headers."""
    token = create_access_token(data={"sub": str(test_user.id), "role": test_user.role})
    return {"Authorization": f"Bearer {token}"}


def test_create_task(auth_headers, test_project):
    """Test task creation."""
    response = client.post(
        "/api/v1/tasks",
        headers=auth_headers,
        json={
            "project_id": str(test_project.id),
            "title": "Test Task",
            "description": "A test task",
            "priority": "HIGH",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "OPEN"


def test_list_tasks(auth_headers, test_project, test_user):
    """Test listing tasks."""
    response = client.get(
        "/api/v1/tasks",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
