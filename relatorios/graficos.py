import matplotlib.pyplot as plt
import pandas as pd
import os

def gerar_grafico(dados: pd.DataFrame, periodo: str) -> str:
    col_numerica = dados.select_dtypes(include='number').columns
    if col_numerica.empty:
        return ""

    caminho = f"grafico_{periodo}.png"
    plt.figure(figsize=(6, 3))
    dados[col_numerica].mean().plot(kind='bar', color='skyblue')
    plt.title(f"Média dos Dados - {periodo.capitalize()}")
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close()
    return caminho