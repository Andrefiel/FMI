import json
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QCheckBox
)

CONFIG_FILE = "config.json"

class ConfigTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.path_input = QLineEdit()
        self.logo_input = QLineEdit()
        self.smtp_host = QLineEdit()
        self.smtp_port = QLineEdit()
        self.smtp_email = QLineEdit()
        self.smtp_pass = QLineEdit()
        self.smtp_tls = QCheckBox("Usar TLS")

        self.load_config()

        self.layout.addWidget(QLabel("📁 Pasta para Monitorar:"))
        self.layout.addWidget(self.path_input)
        path_btn = QPushButton("Selecionar Pasta")
        path_btn.clicked.connect(self.select_folder)
        self.layout.addWidget(path_btn)

        self.layout.addWidget(QLabel("🖼️ Logo da Empresa:"))
        self.layout.addWidget(self.logo_input)
        logo_btn = QPushButton("Selecionar Logo")
        logo_btn.clicked.connect(self.select_logo)
        self.layout.addWidget(logo_btn)

        self.layout.addWidget(QLabel("📧 SMTP Host:"))
        self.layout.addWidget(self.smtp_host)
        self.layout.addWidget(QLabel("SMTP Porta:"))
        self.layout.addWidget(self.smtp_port)
        self.layout.addWidget(QLabel("Email de Envio:"))
        self.layout.addWidget(self.smtp_email)
        self.layout.addWidget(QLabel("Senha:"))
        self.layout.addWidget(self.smtp_pass)
        self.layout.addWidget(self.smtp_tls)

        save_btn = QPushButton("💾 Salvar Configurações")
        save_btn.clicked.connect(self.save_config)
        self.layout.addWidget(save_btn)

        self.setLayout(self.layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecionar pasta para monitorar")
        if folder:
            self.path_input.setText(folder)

    def select_logo(self):
        logo, _ = QFileDialog.getOpenFileName(self, "Selecionar imagem", "", "Imagens (*.png *.jpg *.ico)")
        if logo:
            self.logo_input.setText(logo)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                self.path_input.setText(config.get("monitor_path", ""))
                self.logo_input.setText(config.get("company_logo", ""))
                smtp = config.get("smtp", {})
                self.smtp_host.setText(smtp.get("host", ""))
                self.smtp_port.setText(str(smtp.get("port", "")))
                self.smtp_email.setText(smtp.get("email", ""))
                self.smtp_pass.setText(smtp.get("password", ""))
                self.smtp_tls.setChecked(smtp.get("use_tls", True))

    def save_config(self):
        config = {
            "monitor_path": self.path_input.text(),
            "company_logo": self.logo_input.text(),
            "smtp": {
                "host": self.smtp_host.text(),
                "port": int(self.smtp_port.text()) if self.smtp_port.text().isdigit() else 587,
                "email": self.smtp_email.text(),
                "password": self.smtp_pass.text(),
                "use_tls": self.smtp_tls.isChecked()
            }
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
