import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import pandas as pd
from .analise_dados import gerar_resumo_estatistico
from .graficos import gerar_grafico
from .utils import carregar_config

def gerar_relatorio_pdf(dados: pd.DataFrame, periodo: str, caminho_arquivo: str):
    config = carregar_config()
    logo_path = config.get("logo_path", "")
    titulo = f"Relatório {periodo.capitalize()} - {datetime.now().strftime('%d/%m/%Y')}"

    c = canvas.Canvas(caminho_arquivo, pagesize=A4)
    width, height = A4

    if logo_path and os.path.exists(logo_path):
        c.drawImage(logo_path, 40, height - 80, width=100, preserveAspectRatio=True)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, height - 50, titulo)

    resumo = gerar_resumo_estatistico(dados)
    styles = getSampleStyleSheet()
    y = height - 100
    for linha in resumo:
        p = Paragraph(linha, styles['Normal'])
        p.wrapOn(c, width - 100, 50)
        p.drawOn(c, 50, y)
        y -= 20

    # Gerar e inserir gráfico
    grafico_path = gerar_grafico(dados, periodo)
    if os.path.exists(grafico_path):
        c.drawImage(grafico_path, 100, y - 250, width=400, height=200)

    c.save()