from fastapi import APIRouter, HTTPException
from typing import Optional, List

from models.reserva import ReservaInput

router = APIRouter()

reservas = [
    {"id": 1, "mesa": 5, "nome": "Silva", "pessoas": 4, "ativa": True},
    {"id": 2, "mesa": 3, "nome": "Costa", "pessoas": 2, "ativa": False},
]

@router.get("/", response_model=List[dict])
async def listar_reservas(apenas_ativas: bool = False):
    if apenas_ativas:
        return [r for r in reservas if r["ativa"]]
    return reservas

@router.get("/{reserva_id}")
async def buscar_reserva(reserva_id: int):
    for r in reservas:
        if r["id"] == reserva_id:
            return r
    raise HTTPException(status_code=404, detail="Reserva não encontrada")

@router.get("/mesa/{numero}")
async def reservas_por_mesa(numero: int):
    resultado = [r for r in reservas if r["mesa"] == numero]
    return resultado

@router.post("/", status_code=201)
async def criar_reserva(reserva: ReservaInput):
    mesa_ocupada = any(r["mesa"] == reserva.mesa and r.get("ativa", True) for r in reservas)
    if mesa_ocupada:
        raise HTTPException(status_code=400, detail=f"Mesa {reserva.mesa} já está reservada")
    
    nova = {"id": len(reservas) + 1, **reserva.model_dump(), "ativa": True}
    reservas.append(nova)
    return nova

@router.delete("/{reserva_id}")
async def cancelar_reserva(reserva_id: int):
    for r in reservas:
        if r["id"] == reserva_id:
            r["ativa"] = False
            return {"mensagem": "Reserva cancelada com sucesso"}
    raise HTTPException(status_code=404, detail="Reserva não encontrada")