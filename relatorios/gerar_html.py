import pandas as pd
from datetime import datetime
from .analise_dados import gerar_resumo_estatistico
from .graficos import gerar_grafico
from .utils import carregar_config
import os

def gerar_relatorio_html(dados: pd.DataFrame, periodo: str, caminho_arquivo: str):
    config = carregar_config()
    logo_path = config.get("logo_path", "")
    titulo = f"Relatório {periodo.capitalize()} - {datetime.now().strftime('%d/%m/%Y')}"

    resumo = gerar_resumo_estatistico(dados)
    grafico_path = gerar_grafico(dados, periodo)

    html = f"""
    <html>
    <head>
        <meta charset='utf-8'>
        <title>{titulo}</title>
        <style>
            body {{ font-family: Arial; margin: 30px; }}
            h1 {{ color: #333; }}
            .resumo p {{ margin: 5px 0; }}
        </style>
    </head>
    <body>
        {f'<img src="{logo_path}" height="80">' if logo_path and os.path.exists(logo_path) else ''}
        <h1>{titulo}</h1>
        <div class='resumo'>
            {''.join([f'<p>{linha}</p>' for linha in resumo])}
        </div>
        {f'<img src="{grafico_path}" width="500">' if os.path.exists(grafico_path) else ''}
    </body>
    </html>
    """

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(html)