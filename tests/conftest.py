# tests/conftest.py
import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from app.main import app, engine


@pytest.fixture(autouse=True)
def reset_db():
    # Clean schema for every test
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


@pytest.fixture
def client():
    # Use context manager so startup/shutdown events run
    with TestClient(app) as c:
        yield c
