import pytest

@pytest.mark.smoke
def test_pytest_funcionando():
    assert 1 + 1 == 2

@pytest.mark.smoke
def test_raiz_retorna_bella_tavola(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["restaurante"] == "Bella Tavola"

@pytest.mark.smoke
def test_raiz_retorna_chef(client):
    response = client.get("/")
    assert response.json()["chef"] == "Marco Rossi"
