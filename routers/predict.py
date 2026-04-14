# routers/predict.py

from fastapi import APIRouter
from pydantic import BaseModel, Field
import numpy as np

router = APIRouter()

# Repositório do modelo
REPO_ID = "andersoncda77/bella-tavola-sobremesa-v1"

# Variável global para carregar o modelo apenas uma vez
_model = None

def get_model():
    global _model
    if _model is None:
        from model_utils import load_model
        _model = load_model(REPO_ID)
    return _model


class PredictInput(BaseModel):
    valor_prato_principal: float = Field(gt=0, description="Valor do prato principal")
    horario_pedido: int = Field(ge=0, le=23, description="Hora do pedido (0-23)")
    valor_total_pedido: float = Field(gt=0, description="Valor total da conta")
    quantidade_itens: int = Field(ge=1, description="Quantidade de itens")
    dia_da_semana: int = Field(ge=0, le=6, description="Dia da semana (0=segunda)")
    cliente_frequente: int = Field(ge=0, le=1, description="1 = cliente frequente")


class PredictOutput(BaseModel):
    prediction: int
    probability: float
    label: str
    model_version: str


@router.post("/predict", response_model=PredictOutput)
async def predict(input_data: PredictInput):
    model = get_model()

    features = np.array([[
        input_data.valor_prato_principal,
        input_data.horario_pedido,
        input_data.valor_total_pedido,
        input_data.quantidade_itens,
        input_data.dia_da_semana,
        input_data.cliente_frequente
    ]])

    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][1])
    label = "Pediu sobremesa" if prediction == 1 else "Não pediu sobremesa"

    return PredictOutput(
        prediction=prediction,
        probability=round(probability, 4),
        label=label,
        model_version=REPO_ID
    )