from pydantic import BaseModel, Field
from typing import Optional

class PratoInput(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    categoria: str = Field(pattern="^(pizza|massa|sobremesa|entrada|salada)$")
    preco: float = Field(gt=0)
    descricao: Optional[str] = Field(default=None, max_length=500)
    disponivel: bool = True


class DisponibilidadeInput(BaseModel):
    disponivel: bool


class PratoOutput(BaseModel):
    id: int
    nome: str
    categoria: str
    preco: float
    descricao: Optional[str] = None
    disponivel: bool
    criado_em: Optional[str] = None