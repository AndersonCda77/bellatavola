# train.py - Bloco 2 - Exercício 2.2 (Serialização)

from data_utils import gerar_dataset_bella_tavola
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

print("="*60)
print("   TREINAMENTO + SERIALIZAÇÃO - BELLA TAVOLA")
print("="*60)

# 1. Gerar os dados
df, X, y = gerar_dataset_bella_tavola(
    n_samples=5000, 
    seed=42, 
    proporcao_pede_sobremesa=0.35
)

# 2. Dividir treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# 3. Treinar o modelo
model = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    class_weight='balanced'
)
model.fit(X_train, y_train)

# 4. Avaliar
y_pred = model.predict(X_test)
print("\nRELATÓRIO DE CLASSIFICAÇÃO")
print(classification_report(y_test, y_pred, 
      target_names=["Não pediu sobremesa", "Pediu sobremesa"]))

# 5. Serializar (salvar) o modelo
model_path = "model.pkl"
joblib.dump(model, model_path)

tamanho_kb = os.path.getsize(model_path) / 1024

print(f"\n✅ Modelo salvo com sucesso em: {model_path}")
print(f"   Tamanho do arquivo: {tamanho_kb:.1f} KB")

# 6. Validar o artefato (carregar e comparar predições)
model_carregado = joblib.load(model_path)

amostra = X_test[:5]
pred_original = model.predict(amostra)
pred_carregado = model_carregado.predict(amostra)

assert (pred_original == pred_carregado).all(), "ERRO: Predições não batem!"

print("\n✅ Validação do artefato: OK")
print(f"Predições de teste: {pred_carregado.tolist()}")
print(f"Probabilidades:\n{model_carregado.predict_proba(amostra).round(3)}")