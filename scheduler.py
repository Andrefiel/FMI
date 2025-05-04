import threading
from datetime import datetime, timedelta
from reports.generate_report import generate_report
from reports.email_sender import send_email_report

class ReportScheduler:
    def __init__(self, get_config_func):
        self.get_config = get_config_func
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self.loop)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False

    def loop(self):
        while self.running:
            config = self.get_config()
            if not config["enabled"]:
                continue

            now = datetime.now()
            next_run = config["next_run"]

            if now >= next_run:
                start = self.get_start_date(config["frequency"])
                end = now.strftime("%Y-%m-%d %H:%M:%S")
                generate_report("relatorio_auto.pdf", config["logo_path"], start, end)
                send_email_report(
                    smtp_settings=config["smtp"],
                    recipient=config["email"],
                    subject="Relatório Automático FMI",
                    body="Segue o relatório agendado.",
                    attachment_path="relatorio_auto.pdf"
                )
                config["next_run"] = self.calculate_next_run(config["frequency"], config["time"])

    def calculate_next_run(self, freq, time_qt):
        now = datetime.now()
        base_time = datetime.combine(now.date(), time_qt.toPyTime())
        if freq == "Diário":
            return base_time + timedelta(days=1)
        elif freq == "Semanal":
            return base_time + timedelta(days=7)
        elif freq == "Mensal":
            return base_time + timedelta(days=30)
        return now + timedelta(days=1)

    def get_start_date(self, freq):
        now = datetime.now()
        if freq == "Diário":
            start = now - timedelta(days=1)
        elif freq == "Semanal":
            start = now - timedelta(days=7)
        elif freq == "Mensal":
            start = now - timedelta(days=30)
        else:
            start = now - timedelta(days=1)
        return start.strftime("%Y-%m-%d %H:%M:%S")
