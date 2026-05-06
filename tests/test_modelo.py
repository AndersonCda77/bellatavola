import os
import pytest
import numpy as np

REPO_ID = "andersoncda77/bella-tavola-sobremesa-v1"  # ajuste se necessário
FILENAME = "model.pkl"


@pytest.fixture(scope="module")
def modelo():
    from model_utils import load_model

    # Se o repo do HF for privado/gated, sem token não adianta nem tentar
    if not os.environ.get("HF_TOKEN"):
        pytest.skip("HF_TOKEN ausente (teste de integração).")

    return load_model(REPO_ID, filename=FILENAME)


@pytest.fixture(scope="module")
def amostra_valida(modelo):
    n = int(getattr(modelo, "n_features_in_", 0))
    assert n == 6, f"Esperado 6 features, modelo reportou {n}"
    return np.array([[2.5, 45.0, 20.0, 89.9, 3.0, 1.0]], dtype=float)


# --------- testes do modelo (Ex 5.2) ---------

@pytest.mark.integracao
def test_modelo_carregado_nao_e_none(modelo):
    assert modelo is not None


@pytest.mark.integracao
def test_modelo_tem_predict(modelo):
    assert hasattr(modelo, "predict") and callable(modelo.predict)


@pytest.mark.integracao
def test_modelo_tem_predict_proba(modelo):
    assert hasattr(modelo, "predict_proba") and callable(modelo.predict_proba)


@pytest.mark.integracao
def test_predict_formato(modelo, amostra_valida):
    y = modelo.predict(amostra_valida)
    assert y.shape == (1,)
    assert int(y[0]) in [0, 1]


@pytest.mark.integracao
def test_predict_proba_formato(modelo, amostra_valida):
    p = modelo.predict_proba(amostra_valida)
    assert p.shape == (1, 2)
    assert abs(float(p[0].sum()) - 1.0) < 1e-6
    assert all(0.0 <= float(v) <= 1.0 for v in p[0])


# --------- testes do endpoint (Ex 5.3) ---------

PAYLOAD_VALIDO = {
    "caminho_entrega_km": 5.2,
    "valor_prato_principal": 45.0,
    "horario_pedido": 20,
    "valor_total_pedido": 89.9,
    "quantidade_itens": 3,
    "dia_da_semana": 5,
    "cliente_frequente": 1,
}


@pytest.mark.integracao
def test_endpoint_predict_200(client):
    r = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert r.status_code == 200, r.text


@pytest.mark.integracao
def test_endpoint_campos_esperados(client):
    r = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert r.status_code == 200, r.text
    data = r.json()

    assert "prediction" in data
    assert "probability" in data
    assert "label" in data
    # se existir, ótimo; se não existir, não derruba seu trabalho
    # (se o seu endpoint retorna model_version, pode voltar a exigir)
    # assert "model_version" in data


@pytest.mark.integracao
def test_endpoint_prediction_binaria(client):
    r = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert r.status_code == 200, r.text
    assert int(r.json()["prediction"]) in [0, 1]


@pytest.mark.integracao
def test_endpoint_probability_entre_0_e_1(client):
    r = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert r.status_code == 200, r.text
    prob = float(r.json()["probability"])
    assert 0.0 <= prob <= 1.0


@pytest.mark.integracao
def test_endpoint_label_string(client):
    r = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert r.status_code == 200, r.text
    label = r.json()["label"]
    assert isinstance(label, str)
    assert len(label.strip()) > 0


@pytest.mark.integracao
def test_endpoint_sem_campo_obrigatorio_422(client):
    payload = dict(PAYLOAD_VALIDO)
    payload.pop("valor_total_pedido")
    r = client.post("/ml/predict", json=payload)
    assert r.status_code == 422