# tests/conftest.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from main import app  # noqa: E402
from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def client():
    return TestClient(app)