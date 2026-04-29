# 🍝 Bella Tavola API + MLOps

**API REST completa** para o restaurante Bella Tavola com integração de **Machine Learning** (previsão de sobremesa).

## ✨ O que tem no projeto

- FastAPI modularizada com APIRouter
- Rotas separadas: `/pratos`, `/bebidas`, `/pedidos`, `/reservas`
- Configuração centralizada com `BaseSettings`
- Modelo de Machine Learning treinado
- Endpoint `POST /ml/predict`
- Modelo publicado no **Hugging Face Hub**

## 🚀 Como executar

```bash
# 1. Ativar ambiente
source .venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar a API
uvicorn main:app --reload