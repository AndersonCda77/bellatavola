from fastapi import APIRouter, HTTPException
from typing import Optional, List
from datetime import datetime

# Importando os modelos da pasta models
from models.prato import PratoInput, DisponibilidadeInput, PratoOutput

router = APIRouter()

# Dados em memória
pratos = [
    {"id": 1, "nome": "Margherita", "categoria": "pizza", "preco": 45.0, "disponivel": True},
    {"id": 2, "nome": "Carbonara", "categoria": "massa", "preco": 52.0, "disponivel": True},
    {"id": 3, "nome": "Lasanha Bolonhesa", "categoria": "massa", "preco": 58.0, "disponivel": True},
    {"id": 4, "nome": "Tiramisù", "categoria": "sobremesa", "preco": 28.0, "disponivel": True},
    {"id": 5, "nome": "Quattro Stagioni", "categoria": "pizza", "preco": 49.0, "disponivel": True},
    {"id": 6, "nome": "Panna Cotta", "categoria": "sobremesa", "preco": 24.0, "disponivel": True},
]

@router.get("/", response_model=List[dict])
async def listar_pratos(
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None
):
    resultado = pratos
    if categoria:
        resultado = [p for p in resultado if p.get("categoria") == categoria]
    if preco_maximo is not None:
        resultado = [p for p in resultado if p["preco"] <= preco_maximo]
    return resultado

@router.get("/{prato_id}", response_model=dict)
async def buscar_prato(prato_id: int):
    for prato in pratos:
        if prato["id"] == prato_id:
            return prato
    raise HTTPException(status_code=404, detail=f"Prato com id {prato_id} não encontrado")

@router.post("/", response_model=PratoOutput, status_code=201)
async def criar_prato(prato: PratoInput):
    novo_id = max((p["id"] for p in pratos), default=0) + 1
    novo_prato = {
        "id": novo_id,
        "criado_em": datetime.now().isoformat(),
        **prato.model_dump()
    }
    pratos.append(novo_prato)
    return novo_prato

@router.put("/{prato_id}/disponibilidade")
async def alterar_disponibilidade(prato_id: int, body: DisponibilidadeInput):
    for prato in pratos:
        if prato["id"] == prato_id:
            prato["disponivel"] = body.disponivel
            return prato
    raise HTTPException(status_code=404, detail="Prato não encontrado")