# data_utils.py - Bloco 4 - Exercício 1.3 (Desafio)

import numpy as np
import pandas as pd
from typing import Tuple

def gerar_dataset_bella_tavola(
    n_samples: int = 2000,
    seed: int = 42,
    proporcao_pede_sobremesa: float = 0.35
) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """
    Gera dataset sintético realista para prever se o cliente vai pedir sobremesa 
    no restaurante Bella Tavola.

    Parâmetros
    ----------
    n_samples : int
        Quantidade de pedidos (amostras) a gerar.
    seed : int
        Seed para reprodutibilidade dos dados.
    proporcao_pede_sobremesa : float
        Proporção de clientes que pedem sobremesa (deve estar entre 0.05 e 0.95).

    Retorna
    -------
    df : pd.DataFrame
        DataFrame completo com features e target.
    X : np.ndarray
        Matriz de features (para treinar o modelo).
    y : np.ndarray
        Vetor com o target (0 = não pediu, 1 = pediu sobremesa).

    Exemplo
    -------
    >>> df, X, y = gerar_dataset_bella_tavola(n_samples=1000, seed=42)
    >>> df.shape
    (1000, 7)
    """
    if not (0.05 <= proporcao_pede_sobremesa <= 0.95):
        raise ValueError(
            f"proporcao_pede_sobremesa deve estar entre 0.05 e 0.95. "
            f"Recebido: {proporcao_pede_sobremesa}"
        )

    rng = np.random.default_rng(seed)

    pediu_sobremesa = rng.choice(
        [0, 1],
        size=n_samples,
        p=[1 - proporcao_pede_sobremesa, proporcao_pede_sobremesa]
    )

    valor_prato_principal = np.where(
        pediu_sobremesa,
        rng.uniform(45, 120, n_samples),
        rng.uniform(25, 85, n_samples)
    ).round(2)

    horario_pedido = np.where(
        pediu_sobremesa,
        rng.integers(18, 23, n_samples),
        rng.integers(11, 22, n_samples)
    )

    valor_total_pedido = valor_prato_principal + np.where(
        pediu_sobremesa,
        rng.uniform(20, 45, n_samples),
        rng.uniform(0, 10, n_samples)
    ).round(2)

    quantidade_itens = np.where(
        pediu_sobremesa,
        rng.integers(2, 5, n_samples),
        rng.integers(1, 3, n_samples)
    )

    dia_da_semana = rng.integers(0, 7, n_samples)
    cliente_frequente = rng.choice([0, 1], size=n_samples, p=[0.7, 0.3])

    df = pd.DataFrame({
        "valor_prato_principal": valor_prato_principal,
        "horario_pedido": horario_pedido,
        "valor_total_pedido": valor_total_pedido,
        "quantidade_itens": quantidade_itens,
        "dia_da_semana": dia_da_semana,
        "cliente_frequente": cliente_frequente,
        "pediu_sobremesa": pediu_sobremesa
    })

    X = df.drop(columns=["pediu_sobremesa"]).values
    y = df["pediu_sobremesa"].values

    # Mostrar resumo ao executar diretamente
    print(f"✅ Dataset Bella Tavola gerado: {n_samples} amostras")
    print(f"Proporção que pediu sobremesa: {proporcao_pede_sobremesa:.1%}")
    print("\nMédias por classe:")
    print(df.groupby("pediu_sobremesa").mean().round(2))

    return df, X, y


# ====================== TESTE ======================
if __name__ == "__main__":
    print("=== Gerando dataset Bella Tavola ===\n")
    df, X, y = gerar_dataset_bella_tavola(n_samples=2000, seed=42, proporcao_pede_sobremesa=0.35)
    
    print(f"\nShape do DataFrame: {df.shape}")
    print(f"Shape de X: {X.shape} | Shape de y: {y.shape}")