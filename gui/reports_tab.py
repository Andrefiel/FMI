import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from jinja2 import Template
import os

class ReportTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.label = QLabel("Relatório de Eventos")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.db_path = 'monitoring_data.db'  # Caminho para o seu banco de dados
        self.load_data()

    def load_data(self):
        """ Carrega dados do banco de dados e gera os gráficos """
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect(self.db_path)

        # Verificar as colunas da tabela 'monitoring_events'
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(monitoring_events);")
        columns = cursor.fetchall()

        # Exibir as colunas para depuração
        print("Colunas da tabela 'monitoring_events':")
        for column in columns:
            print(f"Coluna: {column[1]}")

        # Suponhamos que as colunas sejam 'created', 'modified' e 'deleted' (ajuste conforme necessário)
        query = "SELECT * FROM monitoring_events"
        df = pd.read_sql(query, conn)

        # Se as colunas existirem, gera o gráfico
        if 'created' in df.columns and 'modified' in df.columns and 'deleted' in df.columns:
            df[['created', 'modified', 'deleted']].plot(kind='bar')

            plt.title("Monitoramento de Eventos")
            plt.xlabel("Data")
            plt.ylabel("Quantidade de Eventos")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Exibir o gráfico
            plt.show()
        else:
            print("As colunas 'created', 'modified' e 'deleted' não estão presentes na tabela!")

        # Fechar a conexão
        conn.close()

    def generate_report(self):
        """ Gerar relatório em HTML usando Jinja2 """
        # Definindo o modelo do relatório
        html_template = """
        <html>
        <head><title>Relatório de Eventos</title></head>
        <body>
            <h1>Relatório de Monitoramento</h1>
            <p>Aqui estão as estatísticas de monitoramento:</p>
            <table border="1">
                <tr>
                    <th>Evento</th>
                    <th>Quantidade</th>
                </tr>
                <tr>
                    <td>Criações</td>
                    <td>{{ created_count }}</td>
                </tr>
                <tr>
                    <td>Alterações</td>
                    <td>{{ modified_count }}</td>
                </tr>
                <tr>
                    <td>Exclusões</td>
                    <td>{{ deleted_count }}</td>
                </tr>
            </table>
        </body>
        </html>
        """

        # Dados de exemplo (ajuste conforme os dados reais)
        data = {
            'created_count': 100,
            'modified_count': 50,
            'deleted_count': 20
        }

        # Criando o template e renderizando
        template = Template(html_template)
        html_output = template.render(data)

        # Salvando o relatório em HTML
        with open('relatorio_eventos.html', 'w') as file:
            file.write(html_output)

        print("Relatório HTML gerado com sucesso!")

