cat > README.md << 'EOF'
# Bella Tavola API + MLOps

API REST completa para o restaurante Bella Tavola com integração de Machine Learning (previsão de sobremesa).

## Como executar

```bash
source .venv/bin/activate
uvicorn main:app --reload