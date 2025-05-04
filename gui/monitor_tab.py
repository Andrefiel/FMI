from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from file_monitor import FileMonitor
from config_loader import load_config

class MonitorTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.status_label = QLabel("⏹ Monitoramento parado")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.layout.addWidget(self.status_label)

        self.toggle_button = QPushButton("▶ Iniciar Monitoramento")
        self.toggle_button.clicked.connect(self.toggle_monitoring)
        self.layout.addWidget(self.toggle_button)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.layout.addWidget(self.log_output)

        self.monitor = None
        self.monitoring = False

        self.setLayout(self.layout)

    def toggle_monitoring(self):
        if not self.monitoring:
            config = load_config()
            path = config.get("monitor_path", "")
            if not path:
                self.log_output.append("⚠️ Caminho de monitoramento não definido na aba Configurações.")
                return

            self.monitor = FileMonitor(path, callback=self.display_log)
            self.monitor.start()
            self.monitoring = True
            self.status_label.setText("🟢 Monitoramento iniciado")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            self.toggle_button.setText("⏹ Parar Monitoramento")
            self.log_output.append(f"🟢 Monitorando: {path}")
        else:
            if self.monitor:
                self.monitor.stop()
            self.monitoring = False
            self.status_label.setText("⏹ Monitoramento parado")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.toggle_button.setText("▶ Iniciar Monitoramento")
            self.log_output.append("🛑 Monitoramento encerrado.")

    def display_log(self, message):
        self.log_output.append(message)
