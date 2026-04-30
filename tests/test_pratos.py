import pytest

def test_listar_pratos_retorna_200(client):
    response = client.get("/pratos")
    assert response.status_code == 200

def test_listar_pratos_retorna_lista(client):
    response = client.get("/pratos")
    assert isinstance(response.json(), list)

def test_listar_pratos_retorna_pelo_menos_um(client):
    response = client.get("/pratos")
    assert len(response.json()) > 0

def test_pratos_tem_campos_obrigatorios(client):
    response = client.get("/pratos")
    assert response.status_code == 200
    pratos = response.json()
    assert len(pratos) > 0
    p0 = pratos[0]
    for campo in ["id", "nome", "categoria", "preco", "disponivel"]:
        assert campo in p0

def test_filtro_categoria_pizza(client):
    response = client.get("/pratos?categoria=pizza")
    assert response.status_code == 200
    for prato in response.json():
        assert prato["categoria"] == "pizza"

def test_buscar_prato_existente_retorna_200(client):
    response = client.get("/pratos/1")
    assert response.status_code == 200

def test_buscar_prato_existente_tem_campos(client):
    response = client.get("/pratos/1")
    assert response.status_code == 200
    prato = response.json()
    assert "id" in prato and "nome" in prato and "preco" in prato

def test_buscar_prato_inexistente_retorna_404(client):
    response = client.get("/pratos/9999")
    assert response.status_code == 404

def test_criar_prato_valido(client):
    novo_prato = {
        "nome": "Funghi Trifolati Teste",
        "categoria": "massa",
        "preco": 54.0,
        "disponivel": True
    }
    response = client.post("/pratos", json=novo_prato)
    assert response.status_code in [200, 201]
    dados = response.json()
    assert "id" in dados
    assert dados["nome"] == "Funghi Trifolati Teste"

def test_criar_prato_com_preco_negativo_retorna_422(client):
    response = client.post("/pratos", json={
        "nome": "Prato Invalido",
        "categoria": "pizza",
        "preco": -10.0
    })
    assert response.status_code == 422

def test_criar_prato_com_nome_curto_retorna_422(client):
    response = client.post("/pratos", json={
        "nome": "AB",
        "categoria": "pizza",
        "preco": 40.0
    })
    assert response.status_code == 422

def test_criar_prato_com_categoria_invalida_retorna_422(client):
    response = client.post("/pratos", json={
        "nome": "Prato Exotico",
        "categoria": "esoterico",
        "preco": 40.0
    })
    assert response.status_code == 422

def test_prato_criado_aparece_na_listagem(client):
    nome_unico = "Tagliatelle Teste XYZ-9871"
    client.post("/pratos", json={
        "nome": nome_unico,
        "categoria": "massa",
        "preco": 68.0
    })
    response = client.get("/pratos")
    nomes = [p["nome"] for p in response.json()]
    assert nome_unico in nomes

@pytest.mark.parametrize("categoria_invalida", [
    "esoterico",
    "fastfood",
    "japonesa",
    "PIZZA",
    "massa extra",
])
def test_categoria_invalida_retorna_422(client, categoria_invalida):
    response = client.post("/pratos", json={
        "nome": "Prato Teste",
        "categoria": categoria_invalida,
        "preco": 40.0
    })
    assert response.status_code == 422

@pytest.mark.parametrize("id_inexistente", [9999, 123456, 99999])
def test_prato_inexistente_retorna_404(client, id_inexistente):
    response = client.get(f"/pratos/{id_inexistente}")
    assert response.status_code == 404

@pytest.mark.parametrize("categoria_valida", [
    "pizza",
    "massa",
    "sobremesa",
    "entrada",
    "salada",
])
def test_filtro_por_categoria_valida(client, categoria_valida):
    response = client.get(f"/pratos?categoria={categoria_valida}")
    assert response.status_code == 200
    for prato in response.json():
        assert prato["categoria"] == categoria_valida
