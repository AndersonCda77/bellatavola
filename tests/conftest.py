import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def prato_valido():
    return {
        "nome": "Prato de Fixture",
        "categoria": "massa",
        "preco": 45.0,
        "disponivel": True
    }

@pytest.fixture
def bebida_valida():
    return {
        "nome": "Agua de Fixture",
        "tipo": "agua",
        "preco": 8.0,
        "alcoolica": False,
        "volume_ml": 500
    }
