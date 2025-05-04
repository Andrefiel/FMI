from PyQt5 import QtWidgets, QtGui, QtCore
import sys

class MonitorTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Botões de controle
        control_layout = QtWidgets.QHBoxLayout()
        self.start_button = QtWidgets.QPushButton("Iniciar Monitoramento")
        self.stop_button = QtWidgets.QPushButton("Parar Monitoramento")
        self.stop_button.setEnabled(False)
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)

        layout.addLayout(control_layout)

        # Tabela de eventos
        self.table = QtWidgets.QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Tipo", "Caminho", "Usuário", "Timestamp"])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def add_event(self, event_type, path, user, timestamp):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(event_type))
        self.table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(path))
        self.table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(user))
        self.table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(timestamp))


class ReportTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Relatórios serão configurados aqui..."))


class ConfigTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QFormLayout()

        self.folder_input = QtWidgets.QLineEdit()
        self.logo_input = QtWidgets.QLineEdit()
        self.smtp_server_input = QtWidgets.QLineEdit()
        self.smtp_port_input = QtWidgets.QSpinBox()
        self.smtp_port_input.setMaximum(65535)
        self.smtp_user_input = QtWidgets.QLineEdit()
        self.smtp_pass_input = QtWidgets.QLineEdit()
        self.smtp_pass_input.setEchoMode(QtWidgets.QLineEdit.Password)

        layout.addRow("Pasta a Monitorar:", self.folder_input)
        layout.addRow("Logo da Empresa:", self.logo_input)
        layout.addRow("SMTP Servidor:", self.smtp_server_input)
        layout.addRow("SMTP Porta:", self.smtp_port_input)
        layout.addRow("SMTP Usuário:", self.smtp_user_input)
        layout.addRow("SMTP Senha:", self.smtp_pass_input)

        self.setLayout(layout)


class FMIApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FMI - File Monitor Inspector")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QtWidgets.QTabWidget()
        self.monitor_tab = MonitorTab()
        self.report_tab = ReportTab()
        self.config_tab = ConfigTab()

        self.tabs.addTab(self.monitor_tab, "Monitoramento")
        self.tabs.addTab(self.report_tab, "Relatórios")
        self.tabs.addTab(self.config_tab, "Configurações")

        self.setCentralWidget(self.tabs)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FMIApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
