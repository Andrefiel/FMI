import sys
from PyQt5.QtCore import QTimer, Qt, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction, QTabWidget, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton
from gui.monitor_tab import MonitorTab
from gui.reports_tab import ReportsTab
from gui.config_tab import ConfigTab
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FMI - Monitoramento de Arquivos')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("assets/icon.ico"))

        # Criando as guias
        self.tabs = QTabWidget(self)
        self.monitor_tab = MonitorTab()
        self.reports_tab = ReportsTab()
        self.config_tab = ConfigTab()

        self.tabs.addTab(self.monitor_tab, "Monitoramento")
        self.tabs.addTab(self.reports_tab, "Relatórios")
        self.tabs.addTab(self.config_tab, "Configurações")

        self.setCentralWidget(self.tabs)

        # Adicionando ícone na bandeja do sistema
        self.tray_icon = QSystemTrayIcon(QIcon("assets/icon.ico"), self)
        self.tray_icon.setToolTip("FMI - Monitoramento de Arquivos")

        tray_menu = QMenu(self)
        open_action = QAction("Abrir", self)
        quit_action = QAction("Sair", self)
        quit_action.triggered.connect(self.close)
        open_action.triggered.connect(self.showWindow)

        tray_menu.addAction(open_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Conectar evento de fechar com a bandeja (minimizar ao invés de fechar)
        self.setWindowFlags(self.windowFlags() | Qt.Tool)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def closeEvent(self, event):
        # Fechar o aplicativo completamente
        self.tray_icon.hide()  # Esconde o ícone da bandeja
        event.accept()  # Aceita o fechamento do evento

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.showWindow()  # Reexibe a janela principal

    def showWindow(self):
        # Mostrar a janela quando o ícone da bandeja for clicado
        self.showNormal()  # Torna a janela visível e normal
        self.raise_()       # Coloca a janela no topo
        self.activateWindow()  # Ativa a janela (dá foco a ela)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                # Minimiza para bandeja quando a janela é minimizada
                self.hide()
                self.tray_icon.showMessage("Aplicativo em Segundo Plano", "O aplicativo foi minimizado para a bandeja.")
            else:
                super().changeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
