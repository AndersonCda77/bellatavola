from pydantic import BaseModel, Field

class ReservaInput(BaseModel):
    mesa: int = Field(ge=1, le=20)
    nome: str = Field(min_length=2, max_length=100)
    pessoas: int = Field(ge=1, le=20)