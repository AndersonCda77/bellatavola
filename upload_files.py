# upload_files.py

from huggingface_hub import HfApi
import sklearn
import joblib
import os

print("=== Upload dos arquivos - Bella Tavola ===\n")

api = HfApi()
repo_id = "andersoncda77/bella-tavola-sobremesa-v1"

# Criar requirements.txt limpo
with open("requirements.txt", "w") as f:
    f.write(f"""scikit-learn=={sklearn.__version__}
joblib=={joblib.__version__}
numpy=={__import__('numpy').__version__}
pandas=={__import__('pandas').__version__}
""")

print("✅ requirements.txt criado")

# Arquivos para upload
files = ["model.pkl", "README.md", "requirements.txt"]

for filename in files:
    if os.path.exists(filename):
        api.upload_file(
            path_or_fileobj=filename,
            path_in_repo=filename,
            repo_id=repo_id,
            repo_type="model",
            commit_message=f"Add {filename}"
        )
        print(f"✅ {filename} enviado com sucesso")
    else:
        print(f"⚠️ Arquivo não encontrado: {filename}")

print(f"\n🎉 Upload finalizado!")
print(f"Link do modelo: https://huggingface.co/{repo_id}")