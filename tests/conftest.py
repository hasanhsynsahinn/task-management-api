"""Pytest configuration and fixtures."""

import os
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings
from app.db.session import get_db
from app.main import app
from app.models.base import Base

# Create test database
test_database_url = os.getenv(
    "DATABASE_URL",
    "sqlite:///./test.db"
)

engine = create_engine(
    test_database_url,
    connect_args={"check_same_thread": False} if "sqlite" in test_database_url else {},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator:
    """Database fixture."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session):
    """Test client fixture."""
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    from fastapi.testclient import TestClient
    return TestClient(app)
