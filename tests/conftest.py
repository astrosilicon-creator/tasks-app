# tests/conftest.py
import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

# Use a separate DB for tests
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

# Ensure tests can import from the repo root (the folder that contains 'app/')
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app, engine  # noqa: E402  <-- import after setup on purpose


@pytest.fixture(autouse=True)
def reset_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
