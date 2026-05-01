def test_contrato_get_prato(client):
    response = client.get("/pratos/1")
    assert response.status_code == 200
    prato = response.json()

    campos_obrigatorios = {"id", "nome", "categoria", "preco", "disponivel"}
    assert campos_obrigatorios.issubset(prato.keys())

    assert isinstance(prato["id"], int)
    assert isinstance(prato["nome"], str)
    assert isinstance(prato["categoria"], str)
    assert isinstance(prato["preco"], (int, float))
    assert isinstance(prato["disponivel"], bool)

    assert prato["preco"] > 0
    assert len(prato["nome"]) >= 3


def test_contrato_post_prato(client):
    novo = {
        "nome": "Prato Contrato Teste",
        "categoria": "massa",
        "preco": 45.0,
        "disponivel": True,
    }
    response = client.post("/pratos", json=novo)
    assert response.status_code in (200, 201)
    prato = response.json()

    assert "id" in prato and isinstance(prato["id"], int)
    assert prato["nome"] == novo["nome"]
    assert prato["categoria"] == novo["categoria"]
    assert isinstance(prato["preco"], (int, float))


def test_contrato_erro_404(client):
    response = client.get("/pratos/999999")
    assert response.status_code == 404

    corpo = response.json()
    # FastAPI padrão: {"detail": "..."} | handler custom: {"erro": "..."}
    assert "detail" in corpo or "erro" in corpo

    msg = corpo.get("detail") or corpo.get("erro")
    assert isinstance(msg, str)
    assert msg.strip() != ""


def test_contrato_erro_422(client):
    # Payload com erro suficiente pra disparar validação
    response = client.post("/pratos", json={"nome": "X", "preco": -1})
    assert response.status_code == 422

    corpo = response.json()
    # FastAPI padrão: {"detail": [ {loc,msg,type}, ... ]}
    # Handler custom pode vir como {"detalhes": [...]}
    erros = corpo.get("detail") or corpo.get("detalhes")
    assert erros is not None
    assert isinstance(erros, list)
    assert len(erros) > 0

    # Se estiver no formato padrão do FastAPI, valida estrutura de cada item
    if "detail" in corpo:
        for erro in erros:
            assert "loc" in erro
            assert "msg" in erro
            assert isinstance(erro["loc"], list)
            assert isinstance(erro["msg"], str)
            assert erro["msg"].strip() != ""
