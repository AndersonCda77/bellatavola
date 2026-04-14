# model_utils.py

from huggingface_hub import hf_hub_download
import joblib
import time

def load_model(
    repo_id: str = "andersoncda77/bella-tavola-sobremesa-v1",
    filename: str = "model.pkl",
    force_download: bool = False
):
    """
    Carrega o modelo do Hugging Face Hub com cache.
    """
    t0 = time.time()
    
    local_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        force_download=force_download
    )
    
    model = joblib.load(local_path)
    elapsed = time.time() - t0
    
    origem = "Hub (forçado)" if force_download else "cache local"
    print(f"✅ Modelo carregado de {origem} em {elapsed:.2f}s")
    
    return model