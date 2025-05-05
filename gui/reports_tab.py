from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextBrowser,
    QLabel, QComboBox, QMessageBox, QSizePolicy, QFileDialog
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sqlite3
from datetime import datetime, timedelta
import os
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import schedule
import time

class ReportsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()

        # Período do relatório
        period_layout = QHBoxLayout()
        period_label = QLabel("Período:")
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Diário", "Semanal", "Mensal"])
        period_layout.addWidget(period_label)
        period_layout.addWidget(self.period_combo)
        self.layout.addLayout(period_layout)

        # Botões
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("Gerar Relatório")
        self.export_pdf_button = QPushButton("Exportar para PDF")
        self.export_html_button = QPushButton("Exportar para HTML")
        self.send_email_button = QPushButton("Enviar por E-mail")

        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.export_pdf_button)
        button_layout.addWidget(self.export_html_button)
        button_layout.addWidget(self.send_email_button)
        self.layout.addLayout(button_layout)

        # Visualização do relatório
        self.report_view = QTextBrowser()
        self.report_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.report_view)

        # Área de gráficos
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

        # Conexões
        self.generate_button.clicked.connect(self.generate_report)
        self.export_pdf_button.clicked.connect(self.export_pdf)
        self.export_html_button.clicked.connect(self.export_html)
        self.send_email_button.clicked.connect(self.send_email)

        self.current_report_html = ""

        self.start_scheduler()

def generate_report(self):
    period = self.period_combo.currentText()
    since = self.get_period_start(period)

    conn = sqlite3.connect("event_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, event_type, file_path FROM events WHERE timestamp >= ?", (since,))
    rows = cursor.fetchall()
    conn.close()

    created = sum(1 for r in rows if r[1] == "created")
    modified = sum(1 for r in rows if r[1] == "modified")
    deleted = sum(1 for r in rows if r[1] == "deleted")

    # Gerar gráfico
    self.draw_graph(created, modified, deleted)

    # Logo da empresa vinda de config/config.json
    logo_path = ""
    try:
        with open("config/config.json", "r") as f:
            config_data = json.load(f)
            logo_path = config_data.get("company_logo", "")
    except Exception as e:
        print(f"Erro ao carregar config.json: {e}")

    logo_html = f'<img src="{logo_path}" height="50">' if logo_path and os.path.exists(logo_path) else ""

    html = f"""
    <html>
    <body>
        {logo_html}
        <h2>Relatório {period}</h2>
        <p><b>Período a partir de:</b> {since}</p>
        <ul>
            <li><b>Arquivos Criados:</b> {created}</li>
            <li><b>Arquivos Modificados:</b> {modified}</li>
            <li><b>Arquivos Excluídos:</b> {deleted}</li>
            <li><b>Total de eventos:</b> {len(rows)}</li>
        </ul>
        <h3>Eventos Registrados</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr><th>Data/Hora</th><th>Tipo</th><th>Caminho do Arquivo</th></tr>
            {''.join(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>' for r in rows)}
        </table>
    </body>
    </html>
    """

    self.current_report_html = html
    self.report_view.setHtml(html)

    def get_period_start(self, period):
        now = datetime.now()
        if period == "Diário":
            return (now - timedelta(days=1)).isoformat()
        elif period == "Semanal":
            return (now - timedelta(weeks=1)).isoformat()
        elif period == "Mensal":
            return (now - timedelta(days=30)).isoformat()
        return now.isoformat()

    def export_pdf(self):
        try:
            from xhtml2pdf import pisa
        except ImportError:
            QMessageBox.critical(self, "Erro", "Biblioteca xhtml2pdf não instalada. Use 'pip install xhtml2pdf'.")
            return

        if not self.current_report_html:
            QMessageBox.warning(self, "Aviso", "Gere um relatório antes de exportar.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar PDF", "relatorio.pdf", "PDF Files (*.pdf)")
        if not file_path:
            return

        with open(file_path, "wb") as f:
            pisa_status = pisa.CreatePDF(self.current_report_html, dest=f)

        if pisa_status.err:
            QMessageBox.critical(self, "Erro", "Falha ao exportar PDF.")
        else:
            QMessageBox.information(self, "Sucesso", f"PDF salvo em: {file_path}")

    def export_html(self):
        if not self.current_report_html:
            QMessageBox.warning(self, "Aviso", "Gere um relatório antes de exportar.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar HTML", "relatorio.html", "HTML Files (*.html)")
        if not file_path:
            return

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.current_report_html)

        QMessageBox.information(self, "Sucesso", f"HTML salvo em: {file_path}")

    def send_email(self):
        if not self.current_report_html:
            QMessageBox.warning(self, "Aviso", "Gere um relatório antes de enviar.")
            return

        try:
            with open("config.json", "r") as f:
                config = json.load(f)

            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Relatório Automático"
            msg["From"] = config["email"]
            msg["To"] = config["destinatario"]

            msg.attach(MIMEText(self.current_report_html, "html"))

            server = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
            server.starttls()
            server.login(config["email"], config["password"])
            server.sendmail(config["email"], config["destinatario"], msg.as_string())
            server.quit()

            QMessageBox.information(self, "Sucesso", "E-mail enviado com sucesso!")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao enviar e-mail:\n{str(e)}")

    def draw_graph(self, created=0, modified=0, deleted=0):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(["Criados", "Modificados", "Excluídos"], [created, modified, deleted])
        ax.set_title("Resumo de Arquivos")
        self.canvas.draw()

    def start_scheduler(self):
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(1)

        try:
            with open("config/email_schedule.json", "r") as f:
                sched_conf = json.load(f)
                horario = sched_conf.get("horario")
                if horario:
                    schedule.every().day.at(horario).do(self.auto_send_report)
                    thread = threading.Thread(target=run_scheduler, daemon=True)
                    thread.start()

        except Exception as e:
            print(f"Erro no agendamento: {e}")

    def auto_send_report(self):
        self.generate_report()
        self.send_email()
