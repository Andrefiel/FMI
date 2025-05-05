import pandas as pd

def gerar_resumo_estatistico(dados: pd.DataFrame):
    resumo = []
    if dados.empty:
        return ["Sem dados para análise."]

    for coluna in dados.select_dtypes(include='number').columns:
        media = dados[coluna].mean()
        mediana = dados[coluna].median()
        desvio = dados[coluna].std()
        resumo.append(f"<b>{coluna}</b>: média = {media:.2f}, mediana = {mediana:.2f}, desvio = {desvio:.2f}")

    return resumo