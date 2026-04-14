# upload_model.py - Bloco 3 - Exercício 3.1

from huggingface_hub import HfApi

print("=== Bella Tavola - Criando Repositório no Hugging Face ===\n")

api = HfApi()

# Pega o nome de usuário automaticamente
user_info = api.whoami()
username = user_info["name"]

print(f"✅ Logado como: {username}")

# Nome do repositório
repo_id = f"{username}/bella-tavola-sobremesa-v1"

# Cria o repositório (se já existir, não dá erro)
repo_url = api.create_repo(
    repo_id=repo_id,
    repo_type="model",      # importante: é um modelo
    exist_ok=True,
    private=False
)

print(f"\n✅ Repositório criado com sucesso!")
print(f"   Repositório: {repo_id}")
print(f"   Link direto: https://huggingface.co/{repo_id}")