import smtplib
import schedule
import time
from email.message import EmailMessage
import os
from .utils import carregar_config

def enviar_email(destinatario: str, assunto: str, corpo: str, anexos=None):
    config = carregar_config()
    email_remetente = config.get("email")
    senha = config.get("senha")
    servidor = config.get("smtp")
    porta = config.get("porta", 587)

    msg = EmailMessage()
    msg["From"] = email_remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.set_content(corpo)

    anexos = anexos or []
    for caminho in anexos:
        if os.path.exists(caminho):
            with open(caminho, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(caminho)
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    with smtplib.SMTP(servidor, porta) as smtp:
        smtp.starttls()
        smtp.login(email_remetente, senha)
        smtp.send_message(msg)

def agendar_envio(horario: str, funcao_envio):
    schedule.every().day.at(horario).do(funcao_envio)

    while True:
        schedule.run_pending()
        time.sleep(60)